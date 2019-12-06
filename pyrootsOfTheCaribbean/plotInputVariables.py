import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import optparse
# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)

from evaluationScripts.plotVariables import variablePlotter

usage="usage=%prog [options] \n"
usage+="USE: python plotInputVariables.py -i DIR -o DIR -v FILE  --ksscore --scalesignal=OPTION --lumiscale=FLOAT --ratio --ratiotitel=STR --privatework --log"

parser = optparse.OptionParser(usage=usage)

parser.add_option("-o", "--outputdirectory", dest="outputDir",default="plots_InputFeatures",
        help="DIR for output", metavar="outputDir")

parser.add_option("-i", "--inputdirectory", dest="inputDir",default="InputFeatures",
        help="DIR for input", metavar="inputDir")

parser.add_option("-n", "--naming", dest="naming",default="_dnn.h5",
        help="file ending for the samples in preprocessing", metavar="naming")

parser.add_option("-v", "--variableselection", dest="variableSelection",default="example_variables",
        help="FILE for variables used to train DNNs", metavar="variableSelection")

parser.add_option("-l", "--log", dest="log", action = "store_true", default=False,
        help="activate for logarithmic plots", metavar="log")

parser.add_option("-p", "--privatework", dest="privateWork", action = "store_true", default=False,
        help="activate Private Work option", metavar="privateWork")

parser.add_option("-r", "--ratio", dest="ratio", action = "store_true", default=False,
        help="activate ratio plot", metavar="ratio")

parser.add_option("--ratiotitle", dest="ratioTitle", default="#frac{signal}{background}",
        help="STR #frac{PROCESS}{PROCESS}", metavar="title")

parser.add_option("-k", "--ksscore", dest="KSscore", action = "store_true", default=False,
        help="activate KSscore", metavar="KSscore")

parser.add_option("-s", "--scalesignal", dest="scaleSignal", default=-1,
        help="-1 to scale Signal to background Integral, FLOAT to scale Signal with float value, False to not scale Signal",
        metavar="scaleSignal")

parser.add_option("--lumiscale", dest="lumiScale", default=41.5,
        help="FLOAT to scale Luminosity", metavar="lumiScale")

parser.add_option("--corr",dest="correlationMatrix",default=False,action="store_true",
        help="activate plotting of correlation matrix")

(options, args) = parser.parse_args()

#import Variable Selection
if not os.path.isabs(options.variableSelection):
    sys.path.append(basedir+"/variable_sets/")
    variable_set = __import__(options.variableSelection)
elif os.path.exists(options.variableSelection):
    variable_set = __import__(options.variableSelection)
else:
    sys.exit("ERROR: Variable Selection File does not exist!")

#get input directory path
if not os.path.isabs(options.inputDir):
    data_dir = basedir+"/workdir/"+options.inputDir
elif os.path.exists(options.inputDir):
    data_dir=options.inputDir
else:
    sys.exit("ERROR: Input Directory does not exist!")

#get output directory path
if not os.path.isabs(options.outputDir):
    plot_dir = basedir+"/workdir/"+options.outputDir
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
else: 
    plot_dir=options.outputDir
    if not os.path.exists(options.outputDir):
        os.makedirs(plot_dir)
   


weight = "x.puWeight*x.weight_deepjet_medium_nominal*x.weight_lsf"


# plotting options
plotOptions = {
    "ratio":        options.ratio,
    "ratioTitle":   options.ratioTitle,
    "logscale":     options.log,
    "scaleSignal":  float(options.scaleSignal),
    "lumiScale":    float(options.lumiScale),
    "KSscore":      options.KSscore,
    "privateWork":  options.privateWork,
    }
"""
   scaleSignal:
   -1:     scale to background Integral
   float:  scale with float value
   False:  dont scale
"""

# additional variables to plot
additional_variables = [
    "puWeight",
    "weight_deepjet_medium_nominal",
    "weight_lsf",
    ]

# variables that are not plotted
ignored_variables = [
    "puWeight",
    "weight_deepjet_medium_nominal",
    "weight_lsf",
    ]

# initialize plotter
plotter = variablePlotter(
    output_dir      = plot_dir,
    variable_set    = variable_set,
    add_vars        = additional_variables,
    ignored_vars    = ignored_variables,
    plotOptions     = plotOptions,
    eventWeight     = weight
    )

naming = options.naming
# add signal samples
plotter.addSample(
    sampleName      = "singlet",
    sampleFile      = data_dir+"/singlet"+naming,
    plotColor       = ROOT.kOrange+7,
    signalSample    = True,
    XSscaling       = 0.01)

# add background samples
plotter.addSample(
    sampleName      = "t#bar{t} (SL)",
    sampleFile      = data_dir+"/ttsl"+naming,
    plotColor       = ROOT.kAzure+3,
    XSscaling       = 0.45)

plotter.addSample(
    sampleName      = "t#bar{t} (DL)",
    sampleFile      = data_dir+"/ttdl"+naming,
    plotColor       = ROOT.kAzure+8,
    XSscaling       = 0.11)

# add JT categories
plotter.addCategory("inclusive")


# perform plotting routine
plotter.plot(saveKSValues = options.KSscore, plotCorrelationMatrix = options.correlationMatrix)
