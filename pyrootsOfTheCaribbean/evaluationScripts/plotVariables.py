import ROOT
import os
import sys
import pandas 
import numpy as np
# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(os.path.dirname(filedir))
sys.path.append(basedir)

import utils.generateJTcut as JTcut
import plot_configs.setupPlots as setup

class Sample:
    def __init__(self, sampleName, sampleFile, signalSample = False, filled = None, XSscaling = 1., plotColor = None, apply_cut = True, maxEntries = None):
        self.sampleName = sampleName
        self.sampleFile = sampleFile
        self.isSignal   = signalSample
        self.applyCut   = apply_cut
        self.XSScale    = XSscaling
        self.filled     = filled
        self.stop       = None if not maxEntries else int(maxEntries)

        self.plotColor  = plotColor
        if self.plotColor == None:
            try:
                self.plotColor = setup.GetPlotColor(self.sampleName)
            except:
                print("no color for sample chosen + sample not in color dictionary")
                self.plotColor = 1

        if self.filled == None:
            self.filled = not signalSample

        self.load()
        self.cut_data   = {}

    def load(self):
        with pandas.HDFStore(self.sampleFile, mode = "r") as store:
            self.data = store.select("data", stop = self.stop)
        print("\tnevents: {}".format(self.data.shape[0]))
        # hack
        self.data["Weight_XS"] = self.data["Weight_XS"].astype(float)

    def cutData(self, cut, variables, lumi_scale):
        # if lumi scale was set to zero set scale to 1
        scale = lumi_scale
        if lumi_scale == 0:
            scale = 1.

        if not self.applyCut or cut in ["inclusive", "SL"]:
            self.cut_data[cut] = self.data
            self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS*x.Weight_GEN_nom*scale)
            return

        # cut events according to JT category
        category_cut = JTcut.getJTstring(cut)

        # only save variables that are needed
        variables += ["Weight_XS", "Weight_GEN_nom"]
        self.cut_data[cut] = self.data.query(category_cut)
        self.cut_data[cut] = self.cut_data[cut][list(set(variables))]

        # add weight entry for scaling
        self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS*x.Weight_GEN_nom*scale*self.XSScale)
            
        

class variablePlotter:
    def __init__(self, output_dir, variable_set, add_vars = [], ignored_vars = [], max_entries = None, plotOptions = {}):
        self.output_dir     = output_dir
        self.variable_set   = variable_set
        self.add_vars       = list(add_vars)
        self.ignored_vars   = list(ignored_vars)
        self.max_entries    = max_entries

        self.samples        = {}
        self.ordered_stack  = []
        self.categories     = []
        self.variableconfig = pandas.read_csv(basedir+'/pyrootsOfTheCaribbean/plot_configs/variableConfig.csv')
        self.variableconfig.set_index('variablename',inplace=True)

        # handle options
        defaultOptions = {
            "ratio":        False,
            "ratioTitle":   None,
            "logscale":     False,
            "scaleSignal":  -1,
            "lumiScale":    1,
            "privateWork":  False,
            "KSscore":      False}

        for key in plotOptions:
            defaultOptions[key] = plotOptions[key]
        self.options = defaultOptions

        if self.options["privateWork"]:
            self.options["scaleSignal"]=-1
            self.options["lumiScale"]=1
        

    def addSample(self, **kwargs):
        print("adding sample: "+str(kwargs["sampleName"]))
        kwargs["maxEntries"] = self.max_entries
        self.samples[kwargs["sampleName"]] = Sample(**kwargs)
        if not self.samples[kwargs["sampleName"]].isSignal:
            self.ordered_stack.append(kwargs["sampleName"])

    def addCategory(self, category):
        print("adding category: {}".format(category))
        self.categories.append(category)

    def getAllVariables(self):
        variables = []
        for key in self.samples:
            variables = list(self.samples[key].data.columns.values)
        variables = list(set(variables+self.add_vars))
        return variables

    def plot(self, saveKSValues = False, plotCorrelationMatrix = False):
        # loop over categories and get list of variables
        for cat in self.categories:
            print("starting with category {}".format(cat))

            cat_dir = self.output_dir+"/"+cat+"/"
            if not os.path.exists(cat_dir):
                os.makedirs(cat_dir)
        
            if saveKSValues:
                ks_file = self.output_dir+"/"+cat+"_KSvalues.csv"
                ks_dict = {}

            # if no variable_set is given, plot all variables in samples
            if self.variable_set == None:
                variables = self.getAllVariables()
            # load list of variables from variable set
            elif cat in self.variable_set.variables:
                variables = list(self.variable_set.variables[cat]) + self.add_vars
            else:
                variables = list(self.variable_set.all_variables) + self.add_vars

            # filter events according to JT category
            for key in self.samples:
                self.samples[key].cutData(cat, variables, self.options["lumiScale"])

            correlations = {}
            # loop over all variables and perform plot each time
            for variable in variables:
                if variable in self.ignored_vars: continue
                print("plotting variable: {}".format(variable))

                # generate plot output name
                plot_name = cat_dir + "/{}.pdf".format(variable)
                plot_name = plot_name.replace("[","_").replace("]","")

                # generate plot
                histInfo = self.histVariable(
                    variable    = variable,
                    plot_name   = plot_name,
                    cat         = cat)

                if saveKSValues:
                    ks_dict[variable] = histInfo["KSScore"]
                if plotCorrelationMatrix:
                    correlations[variable] = {}
                    for v2 in variables:
                        corrFactor = self.getCorrelation(variable, v2, cat)
                        correlations[variable][v2] = corrFactor

            if saveKSValues:
                with open(ks_file, "w") as f:
                    for key, value in sorted(ks_dict.iteritems(), key = lambda (k,v): (v,k)):
                        f.write("{},{}\n".format(key, value))

            if plotCorrelationMatrix:
                outfile = self.output_dir+"/"+cat+"_correlations.pdf"
                self.plotCorrelationMatrix(correlations, cat, outfile)

    def getCorrelation(self, v1, v2, cat):
        v1values = []
        v2values = []
        
        for key in self.samples:
            sample = self.samples[key]
            v1values += list(sample.cut_data[cat][v1].values)
            v2values += list(sample.cut_data[cat][v2].values)

        return np.corrcoef(v1values, v2values)[0, 1]
            
    def plotCorrelationMatrix(self, correlations, cat, outfile):

        ncls = len(correlations)
        varlist = sorted(list(correlations.keys()))
        # init histogram
        cm = ROOT.TH2D("correlationMatrix", "", ncls, 0, ncls, ncls, 0, ncls)
        cm.SetStats(False)
        ROOT.gStyle.SetPaintTextFormat(".2f")


        for xit in range(cm.GetNbinsX()):
            for yit in range(cm.GetNbinsY()):
                cm.SetBinContent(xit+1,yit+1, correlations[varlist[xit]][varlist[yit]])

        cm.GetXaxis().SetTitle("")
        cm.GetYaxis().SetTitle("")

        cm.SetMarkerColor(ROOT.kBlack)

        cm.GetZaxis().SetRangeUser(-1, 1)

        for xit in range(ncls):
            varname = self.variableconfig.loc[varlist[xit],"displayname"]
            cm.GetXaxis().SetBinLabel(xit+1, varname)
        for yit in range(ncls):
            varname = self.variableconfig.loc[varlist[yit],"displayname"]
            cm.GetYaxis().SetBinLabel(yit+1, varname)

        cm.GetXaxis().SetLabelSize(0.025)
        cm.GetXaxis().LabelsOption("v")
        cm.GetYaxis().SetLabelSize(0.025)
        cm.SetMarkerSize(0.6)

        # init canvas
        canvas = ROOT.TCanvas("", "", 5000, 5000)
        canvas.SetTopMargin(0.1)
        canvas.SetBottomMargin(0.3)
        canvas.SetRightMargin(0.12)
        canvas.SetLeftMargin(0.3)
        canvas.SetTicks(1,1)

        # draw histogram
        ROOT.gStyle.SetPalette(ROOT.kRedBlue)
        draw_option = "colz text1"
        cm.DrawCopy(draw_option)

        # setup TLatex
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextColor(ROOT.kBlack)
        latex.SetTextSize(0.03)

        l = canvas.GetLeftMargin()
        t = canvas.GetTopMargin()

        # add category label
        latex.DrawLatex(l+0.001,1.-t+0.01, JTcut.getJTlabel(cat))

        canvas.SaveAs(outfile)
        



    def histVariable(self, variable, plot_name, cat):
        histInfo = {}

        if variable in self.variableconfig.index:
            # get variable info from config file
            bins = int(self.variableconfig.loc[variable,'numberofbins'])
            minValue = float(self.variableconfig.loc[variable,'minvalue'])
            maxValue = float(self.variableconfig.loc[variable,'maxvalue'])
            displayname = self.variableconfig.loc[variable,'displayname']
            logoption = self.variableconfig.loc[variable,'logoption']
        else:
            bins = 30
            maxValue = max([max(self.samples[sample].cut_data[cat][variable].values) for sample in self.samples])
            minValue = min([min(self.samples[sample].cut_data[cat][variable].values) for sample in self.samples])
            displayname = variable
            logoption = "-"

            config_string = "{},{},{},{},{},{}\n".format(variable, minValue, maxValue, bins, logoption, displayname)
            with open("new_variable_configs.csv", "a") as f:
                f.write(config_string)
        
        bin_range = [minValue, maxValue]
        if logoption=="x" or logoption=="X":
            logoption=True
        else:
            logoption=False

        histInfo["nbins"] = bins
        histInfo["range"] = bin_range

        bkgHists = []
        bkgLabels = []
        weightIntegral = 0

        # loop over backgrounds and fill hists
        for sampleName in self.ordered_stack:
            sample = self.samples[sampleName]

            # get weights
            weights = sample.cut_data[cat]["weight"].values
            # get values
            values = sample.cut_data[cat][variable].values

            #weights = [weights[i] for i in range(len(weights)) if not np.isnan(values[i])]
            #values =  [values[i]  for i in range(len(values))  if not np.isnan(values[i])]

            weightIntegral += sum(weights)
            # setup histogram
            hist = setup.setupHistogram(
                values      = values,
                weights     = weights,
                nbins       = bins,
                bin_range   = bin_range,
                color       = sample.plotColor,
                xtitle      = cat+"_"+sample.sampleName+"_"+variable,
                ytitle      = setup.GetyTitle(self.options["privateWork"]),
                filled      = sample.filled)
            bkgHists.append(hist)
            bkgLabels.append(sample.sampleName)

        sigHists = []
        sigLabels = []
        sigScales = []
        
        # if not background was added, the weight integral is equal to 0
        if weightIntegral == 0:
            self.options["scaleSignal"] = 0   
        histInfo["bkgYield"] = weightIntegral

        # scale stack to one if lumiScale is set to zero
        if self.options["lumiScale"] == 0:
            for hist in bkgHists:
                hist.Scale(1./weightIntegral)
            weightIntegral = 1.

        # loop over signals and fill hists
        for key in self.samples:
            sample = self.samples[key]
            if not sample.isSignal: continue

            # get weights
            weights = sample.cut_data[cat]["weight"].values
            # determine scale factor
            if self.options["scaleSignal"] == -1:
                scaleFactor = weightIntegral/(sum(weights)+1e-9)
            elif self.options["scaleSignal"] == 0:
                scaleFactor = (1./(sum(weights)+1e-9))
            else:
                scaleFactor = float(self.options["scaleSignal"])

            # setup histogram
            hist = setup.setupHistogram(
                values      = sample.cut_data[cat][variable].values,
                weights     = weights,
                nbins       = bins,
                bin_range   = bin_range,
                color       = sample.plotColor,
                xtitle      = cat+"_"+sample.sampleName+"_"+variable,
                ytitle      = setup.GetyTitle(),
                filled      = sample.filled)

            hist.Scale(scaleFactor)

            sigHists.append(hist)
            sigLabels.append(sample.sampleName)
            sigScales.append(scaleFactor)

        # init canvas
        canvas = setup.drawHistsOnCanvas(
            sigHists, bkgHists, self.options,   
            canvasName = variable, displayname=displayname,
            logoption = logoption)

        # setup legend
        legend = setup.getLegend()
        # add signal entriesa
        for iSig in range(len(sigHists)):
            labelstring = sigLabels[iSig]       
            if not self.options["lumiScale"] == 0.:
                labelstring = sigLabels[iSig]+" x {:4.0f}".format(sigScales[iSig])

            # add KS score to label if activated
            if self.options["KSscore"]:
                KSscore = setup.calculateKSscore(bkgHists[0],sigHists[iSig])
                labelstring="#splitline{"+labelstring+"}{KSscore = %.3f}"%(KSscore)
                histInfo["KSScore"] = KSscore
                
            legend.AddEntry(sigHists[iSig], labelstring, "L")

        # add background entries
        for iBkg in range(len(bkgHists)):
            legend.AddEntry(bkgHists[iBkg], bkgLabels[iBkg], "F")

        # draw loegend
        legend.Draw("same")

        # add lumi and category to plot
        setup.printLumi(canvas, lumi = self.options["lumiScale"], ratio = self.options["ratio"])
        setup.printCategoryLabel(canvas, JTcut.getJTlabel(cat), ratio = self.options["ratio"])
        if self.options["privateWork"]: 
            setup.printPrivateWork(canvas, ratio = self.options["ratio"])

        # save canvas
        setup.saveCanvas(canvas, plot_name)
    
        return histInfo


