import os
import sys
import optparse

# local imports

filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(os.path.dirname(filedir))
sys.path.append(basedir)
import root2pandas

############################################################################################################

#options for command line

"""
USE: python preprocessing.py --outputdirectory=DIR --variableSelection=FILE --maxentries=INT --MEM=BOOL
"""
usage="usage=%prog [options] \n"
usage+="USE: python preprocessing.py --outputdirectory=DIR --variableselection=FILE --maxentries=INT --MEM=BOOL --name=STR\n"
usage+="OR: python preprocessing.py -o DIR -v FILE -e INT -m BOOL -n STR"

parser = optparse.OptionParser(usage=usage)

parser.add_option("-o", "--outputdirectory", dest="outputDir",default="InputFeatures",
        help="DIR for output", metavar="outputDir")

parser.add_option("-v", "--variableselection", dest="variableSelection",default="example_variables_cnn", #other default example file for cnns
        help="FILE for variables used to train DNNs", metavar="variableSelection")

parser.add_option("-e", "--maxentries", dest="maxEntries", default=50000,
        help="INT used for maximal number of entries for each batch (to restrict memory usage)", metavar="maxEntries")

parser.add_option("-m", "--MEM", dest="MEM", action = "store_true", default=False,
        help="BOOL to use MEM or not", metavar="MEM")

parser.add_option("-n", "--name", dest="Name", default="cnn", #changed default from dnn to cnn
        help="STR of the output file name", metavar="Name")

parser.add_option("-r", "--rotation_cnn", dest="rotation_cnn", default=None,
        help="STR of the desired cnn rotation", metavar="Name")

(options, args) = parser.parse_args()


#right path for output and variable_sets

if not os.path.isabs(options.variableSelection):
    sys.path.append(basedir+"/variable_sets/")
    variable_set = __import__(options.variableSelection)
elif os.path.exists(options.variableSelection):
    variable_set = __import__(options.variableSelection)
else:
    sys.exit("ERROR: Variable Selection File does not exist!")

if not os.path.isabs(options.outputDir):
    outputdir = basedir+"/workdir/"+options.outputDir
elif os.path.exists(options.outputDir) or os.path.exists(os.path.dirname(options.outputDir)):
    outputdir=options.outputDir
else:
    sys.exit("ERROR: Output Directory does not exist!")

##############################################################################################################

#event selection

# define a base event selection which is applied for all Samples
# select only events with GEN weight > 0 because training with negative weights is weird
base = "(N_Jets >= 6 and N_BTagsM >= 3 and Evt_MET_Pt > 20. and Weight_GEN_nom > 0.)"


# single lepton selections
single_mu_sel = "(N_LooseElectrons == 0 and N_TightMuons == 1 and Muon_Pt > 29. and Triggered_HLT_IsoMu27_vX == 1)"
single_el_sel = "(N_LooseMuons == 0 and N_TightElectrons == 1 and (Triggered_HLT_Ele35_WPTight_Gsf_vX == 1 or Triggered_HLT_Ele28_eta2p1_WPTight_Gsf_HT150_vX == 1))"

base_selection = "("+base+" and ("+single_mu_sel+" or "+single_el_sel+"))"


ttH_selection = "(Evt_Odd == 1)"

# define output classes
ttH_categories = root2pandas.EventCategories()
ttH_categories.addCategory("ttH", selection = None)

ttbar_categories = root2pandas.EventCategories()
ttbar_categories.addCategory("ttbar", selection = None)



######################################################################################################
#initaialize data 

# initialize dataset class
dataset = root2pandas.Dataset(
    outputdir   = outputdir,
    naming      = options.Name,
    addMEM      = options.MEM,
    maxEntries  = options.maxEntries)

# add base event selection
dataset.addBaseSelection(base_selection)



ntuplesPath = "/nfs/dust/cms/user/vdlinden/legacyTTH/ntuples/legacy_2018_ttH_newJEC"

# add samples to dataset

dataset.addSample(
    sampleName  = "TTbar",
    ntuples     = ntuplesPath+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/*nominal*.root", #*_2*nominal*
    categories  = ttbar_categories,
    selections  = None, #"(Evt_Odd == 1)" <=for even odd splitting in final form
    )

dataset.addSample(
    sampleName  = "TTH",
    ntuples     = ntuplesPath+"/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/*nominal*.root", #*_2*nominal*
    categories  = ttH_categories,
    selections  = None,#"(Evt_Odd == 1)" <=for even odd splitting in final form #ttbar_selection,
    )

# initialize variable list 
#dataset.addVariables(variable_set.all_variables)

# define an additional variable list
additional_variables = [
    "N_Jets",
    "N_BTagsM",
    "Weight_XS",
    "Weight_CSV",
    "Weight_GEN_nom",
    "Evt_ID", 
    "Evt_Run", 
    "Evt_Lumi"
    ]

# add these variables to the variable list
dataset.addVariables(additional_variables)

#########################################################################################################
#create 2D Image

# pixel size definition
d_eta = 0.4
d_phi = 0.4
# range definitions
eta_range = [-2.4,2.4]
phi_range = [-3.14159265358979, 3.14159265358979]
# pixel converter
n_px_eta = int( (eta_range[1]-eta_range[0])/d_eta )
n_px_phi = int( (phi_range[1]-phi_range[0])/d_phi )
print("creating image with size "+str(n_px_eta)+" x "+str(n_px_phi)+" pixels")
print("using rotation type "+str(options.rotation_cnn))
print(variable_set.all_variables)
# putting above info into following object
imageconfig = root2pandas.ImageConfig(
    x ="Eta", y="Phi",
    channels  = ["Jet_Pt[0-9]", "TaggedJet_Pt[0-9]"],#variable_set.all_variables, #["TaggedJet_Pt[0-9]", "Jet_Pt[0-16]"],# "Electron_Pt[0-9]",
    imageSize = [n_px_eta, n_px_phi],
    xRange    = eta_range,
    yRange    = phi_range,
    rotation  = options.rotation_cnn, #options.rotation_cnn or None or "MaxJetPt" or "ttbar_toplep" or "sphericity_ev1" or "sphericity_ev2" or "sphericity_ev3"
    # pixel intensity linear or logarithmic
    logNorm     = False)

#print(str(len(imageconfig.variables))+" VARIABLES in Image_Config: " + str(imageconfig.variables))
#print(imageconfig.images)

#######################################################################################################

# run the preprocessing
dataset.runPreprocessing(imageconfig)