# global imports
import os
import sys
import pandas as pd
import glob
from collections import Counter
import operator
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
import matplotlib.pyplot as plt
import numpy as np
import optparse


# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)
import generateJTcut
nameConfig = basedir+"/pyrootsOfTheCaribbean/plot_configs/variableConfig.csv"
translationFile = pd.read_csv(nameConfig, sep = ",").set_index("variablename", drop = True)

usage = "python getTopVariables.py [options] [jtCategories]"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-w","--workdir",dest="workdir",default=basedir+"/workdir/",
    help = "path to working directory where trained DNN files are placed")
parser.add_option("-i","--input",dest="inputdir",default="test_training",
    help = "path to DNN directories relative to WORKDIR. add JTSTRING as placeholder\
for jet-tag categories and escaped wildcards ('\*') for multiple DNN runs.")
parser.add_option("-o","--output",dest="outdir",default="./",
    help = "path to output directory e.g. for plots or variable sets")
parser.add_option("-p","--plot",dest="plot",default=False,action="store_true",
    help = "generate plots of variable rankings")
parser.add_option("--nplot",dest="nplot",default=30,type=int,
    help = "number of variables to be plotted (-1 for all).")
parser.add_option("-v","--variableset",dest="generate_variableset",default=False,action="store_true",
    help = "generate new variable set from variable rankings")
parser.add_option("--nvset",dest="nvset",default=30,type=int,
    help = "number of variables written to variable set (-1 for all).")
parser.add_option("-t", "--type", dest = "weight_type",default="absolute",
    help = "type of variable ranking (i.e. name of weight file TYPE_weight_sum.csv), e.g. 'absolute', 'propagated'")

(opts, args) = parser.parse_args()
inputdir = opts.workdir+"/"+opts.inputdir
if not "JTSTRING" in inputdir:
    inputdir+="_JTSTRING/"
print("using input directory {}".format(inputdir))

if not os.path.exists(opts.outdir):
    os.makedirs(opts.outdir)


sorted_variables = {}
for jtcat in args:
    print("\n\nhandling category {}\n\n".format(jtcat))
    jtpath = inputdir.replace("JTSTRING",jtcat)
    
    # collect weight sum files
    jtpath+= "/"+opts.weight_type+"_weight_sums.csv"
    rankings = glob.glob(jtpath)
    print("found {} variable ranking files".format(len(rankings)))

    # collect variables and their relative importance
    variables = {}
    for ranking in rankings:
        csv = pd.read_csv(ranking, header = 0, sep = ",", names = ["variable", "weight_sum"])
        sum_of_weights = csv["weight_sum"].sum()
        for row in csv.iterrows():
            if not row[1][0] in variables: variables[row[1][0]] = []
            variables[row[1][0]].append(100*row[1][1]/sum_of_weights)


    # collect mean values of variables
    mean_dict = {}
    for v in variables: mean_dict[v] = np.median(variables[v])

    # generate lists sorted by mean variable importance
    var = []
    val = []
    mean = []
    std = []
    i = 0
    maxvalue = 0
    for v, m in sorted(mean_dict.iteritems(), key = lambda (k, vl): (vl, k)):
        i += 1
        val.append(i)
        var.append(translationFile.loc[v,"displayname"].replace("#","\\"))
        mean.append(m)
        std.append( np.std(variables[v]) )
        print(v,m)
        if mean[-1]+std[-1] > maxvalue: maxvalue = mean[-1]+std[-1]

    sorted_variables[jtcat] = var

    if opts.plot:
        if not opts.nplot == -1:
            mean = mean[-opts.nplot :]
            val = val[-opts.nplot :]
            std = std[-opts.nplot :]
            var = var[-opts.nplot :]

        nvariables = len(var)
        plt.figure(figsize = [10,nvariables/4])
        plt.errorbar(mean, val, xerr = std, fmt = "o")
        plt.xlim([0.,1.1*maxvalue])
        plt.grid()
        plt.yticks(val, var)
        plt.title(generateJTcut.getJTlabel(jtcat), loc = "right", fontsize = 16)
        plt.xlabel(r"mean of sum of input weights (in percent)", fontsize = 16)
        plt.tight_layout()
        outfile = opts.outdir+"/"+opts.weight_type+"_weight_sums_"+jtcat+".pdf"
        plt.savefig(outfile)
        plt.clf() 
        print("saved plot to {}".format(outfile))

if opts.generate_variableset:
    string = "variables = {}\n"
    for jt in sorted_variables:
        string += "\nvariables[\"{}\"] = [\n".format(jt)

        variables = sorted_variables[jt]
        if not opts.nvset==-1:
            variables = variables[-opts.nvset:]

        for v in variables:
            string += "    \"{}\",\n".format(v)

        string += "    ]\n\n"

    string += "all_variables = list(set( [v for key in variables for v in variables[key] ] ))\n"

    outfile = opts.outdir+"/autogenerated_"+opts.weight_type+"_variableset.py"
    with open(outfile,"w") as f:
        f.write(string)
    print("wrote variable set to {}".format(outfile))
