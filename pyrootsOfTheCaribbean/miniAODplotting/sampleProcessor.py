# import ROOT in batch mode
import sys
import ROOT
import pandas as pd
import numpy as np
import glob
import os
import stat
# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events
filedir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(filedir+"/variableProcessors/")
import readEvent
import copy
import importlib

def importProcessors(processors):
    modules = []
    for processor in processors:
        print("loading {}".format(processor))
        modules.append( importlib.import_module(processor) )
    return modules
    
def processSample(sample, out_path, sample_type = "ttH", XSWeight = 1., processors = []):
    ''' 
    process a single sample
        - sample:       path to root file (mAOD-type)
        - out_path:     path to output hdf5-file
        - sample_type:  what type of sample (ttH/ttZ/ttZll/ttZqq/ttHbb/...)
        - XSWeight:     cross section weight for that sample (used for normalization of plots)   
    '''
    variableProcessors = importProcessors(processors)

    # loading events from file via FWlite 
    events = Events(sample)
    n_events = events.size()
    print("total number of events in file: {}".format(n_events))

    dfs = []

    # counters for bookkeeping stuff
    addb            = 0
    semilep         = 0
    addb_and_sl     = 0
    fromProton      = 0
    fromGluon       = 0
    fromOtherMother = 0
    gluonAndProton  = 0


    # start event loop
    for iev, event in enumerate(events):
        if iev%1000==0: print("#{}".format(iev))
        
        # read all the things from event which is specified in readEvent
        evt = readEvent.readEvent(iev, event, XSWeight, event_type = sample_type)

        # counters
        if evt.hasAddBQuarks: 
            addb += 1
            if evt.fromProton:
                fromProton += 1
            if evt.fromGluon:
                fromGluon += 1
            if evt.fromProton and evt.fromGluon:
                gluonAndProton += 1
            if evt.otherMother:
                fromOtherMother += 1
        if evt.isSemilep: semilep += 1
        if evt.hasAddBQuarks and evt.isSemilep: addb_and_sl += 1

        # check if event passes baseline cuts
        if not evt.passesCuts(): continue




        # calculate variables in variable processors
        for module in variableProcessors:
            module.calculateVariables(evt)

        event_df = pd.DataFrame.from_dict(copy.deepcopy(evt).variables)
        #event_df = variableCalculations.calculateVariables(copy.deepcopy(evt))
        
        # add the variable dictionary (in DataFrame format) to that temporary list
        dfs.append(event_df)
        
    print("number of events with additional B: {}".format(addb))
    print("\tof which {} add b pairs come from protons".format(fromProton))
    print("\tof which {} add b pairs come from gluons".format(fromGluon))
    print("\tof which {} events have both".format(gluonAndProton))
    print("\tof which {} are from other mothers".format(fromOtherMother))
    print("semilep events: {}".format(semilep))
    print("semilep and additional b: {}".format(addb_and_sl))

    # concatenate dataframes
    df = pd.concat(dfs)
    print("number of events passing cuts n stuff: {}".format(df.shape[0]))
        
    # set event indices
    df.set_index(["Evt_Run", "Evt_Lumi", "Evt_ID"], inplace = True, drop = True)

    # save dataframe to output file
    df.to_hdf(out_path, key = "data", mode = "w")
    
    return out_path



def generate_submit_scripts(sample_dict, out_dir, filedir, variableProcessors):
    ''' loop over all the samples in the sample dictionary and create a shellscript for submission to NAF '''

    shellscripts = []
    sample_parts = {}
    # get all specified samples
    for sample in sample_dict:
        # get all mAOD files in that sample
        files = sample_dict[sample]["data"]
        if type(files) == str:
            files = glob.glob(files)

        # get the crosssection weight for that sample
        XSWeight = sample_dict[sample]["XSWeight"]

        outputs = []
        # loop over the files and write the shell script
        for i, f in enumerate(files):
            shell_path, output_file = write_single_script(i, f, out_dir, filedir, sample, XSWeight, variableProcessors)
            shellscripts.append(shell_path)
            outputs.append(output_file)
        sample_parts[sample] = outputs

    return shellscripts, sample_parts

def write_single_script(i, f, out_dir, file_dir, sample, XSWeight, variableProcessors):
    ''' 
    write a shell script for submission to NAF batch system
        - i:        some index for naming
        - f:        mAOD type root file
        - out_dir:  output directory
        - file_dir: base directory of MLFoy
        - sample:   type of sample (needed for some variable definition)
        - XSWeight: cross section weight of that sample
    '''
    # generate directory to save shell scripts 
    shell_path = out_dir + "/shell_scripts/"
    if not os.path.exists(shell_path):
        os.makedirs(shell_path)
    
    # generate path to processor file which is called by shell script
    python_file = file_dir + "/miniAODplotting/processSingleSample.py"
    
    # generate output name of shell script
    shell_path += str(sample)+"_"+str(i)+".sh"

    # generate output name of hdf5 file
    out_file = out_dir + "/h5parts/"
    if not os.path.exists(out_file):
        os.makedirs(out_file)
    out_file += str(sample)+"_"+str(i)+".h5"

    # write script
    script = """
#!/bin/bash
export X509_USER_PROXY={proxy}
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
export SCRAM_ARCH={arch}
cd /nfs/dust/cms/user/vdlinden/CMSSW/CMSSW_9_2_4/src
eval `scram runtime -sh`
cd - 
rm {out_file}
python {python_file} -f {f} -o {out_file} -s {sample} -w {XSWeight} """.format(
        proxy       = os.environ['X509_USER_PROXY'],
        arch        = os.environ['SCRAM_ARCH'],
        python_file = python_file,
        out_file    = out_file,
        f           = f,
        sample      = sample,
        XSWeight    = str(XSWeight))

    script+= " ".join(variableProcessors)
    
    # save shell file
    with open(shell_path, "w") as shf:
        shf.write(script)
    st = os.stat(shell_path)
    os.chmod(shell_path, st.st_mode | stat.S_IEXEC)

    print("wrote shell script "+str(shell_path))
    return shell_path, out_file

def concat_samples(sample_parts, path):
    ''' concatenate all the single files produced by NAF jobs '''

    non_existing_files = []    
    # loop over the samples
    for sample in sample_parts:
        print("concatenating for sample "+str(sample))
        parts = sample_parts[sample]

        # generate output path of concatenated data file
        out_file = path + "/" + sample + ".h5"
        if os.path.exists(out_file):
            os.remove(out_file)

        # start concatenating procedure
        for iPart, p in enumerate(parts):
            print("({}/{}) adding file {}".format(iPart+1,len(parts),p))

            if not os.path.exists(p):
                non_existing_files.append(p)
                print("!!! file does not exist !!!")
                continue

            # load part file
            with pd.HDFStore(p, mode = "r") as store:
                df = store.select("data")
            print("\t{} events.".format(df.shape[0]))
        
            # save to concatenated file
            with pd.HDFStore(out_file, mode = "a") as store:
                store.append("data", df, index = False)
            
    if len(non_existing_files) > 0:
        print("the following files did not exist:")
        for f in non_existing_files: print(f)





