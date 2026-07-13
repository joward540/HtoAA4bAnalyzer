import ROOT
import numpy as np
import os
import glob
from pathlib import Path
import argparse

# Enable multi-threading
#ROOT.ROOT.EnableImplicitMT()





#-------------------------------------------------------------------------------#File load Module------------------------------------------------------------------------------------------#

#Input Directories

#Here is the parent directory with the NanoAOD files we need.
input_dir = Path('/cms/data/store/user/hatake/ParTV2V3_Nanov15_v2')


#Let's save all the relevant subdirectories in dictionaries.
samples = {
    "M30": {
        "subdir": "GluGluH-01J-HToAATo4B_Par-M-30_13p6TeV",
        "pattern": "Summer24NanoAODv15_GluGluH-01J-HToAATo4B_Par-M-30_13p6TeV_job*.root",
        "label": "HToAATo4b M=30",
    },

    "M35": {
        "subdir": "GluGluH-01J-HToAATo4B_Par-M-35_13p6TeV",
        "pattern": "Summer24NanoAODv15_GluGluH-01J-HToAATo4B_Par-M-35_13p6TeV_job*.root",
        "label": "HToAATo4b M=35",
    },

    "QCD0B": {
        "subdir": "QCD0B-4Jets_Bin-HT-800to1000_Fil-BPS_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-800to1000_Fil-BPS_13p6TeV_job*.root",
        "label": "QCD0B HT 800-1000",
    },

    "QCDB": {
        "subdir": "QCDB-4Jets_Bin-HT-800to1000_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCDB-4Jets_Bin-HT-800to1000_13p6TeV_job*.root",
        "label": "QCDB HT 800-1000",
    },
}

#This will allow us to make an argument after calling the script. If we don't include an argument, we'll run for all datasets. If we do include it, we'll only run for one dataset.
parser = argparse.ArgumentParser(description="Make FatJet histograms for HtoAA samples.")

parser.add_argument("dataset", nargs="?", choices=list(samples.keys()), help="Optional dataset to run: M30, M35, QCD0B, or QCDB. If omitted, all datasets run.")
parser.add_argument("--max-files", type=int, default=None, help="Maximumn number of ROOT files to use per dataset for testing.")

args = parser.parse_args()

if args.dataset is None:
    samples_to_run = samples
else:
    samples_to_run = {args.dataset: samples[args.dataset]}



#Directory for test run including off-shell variables.
#/cms/data/juward/ana/Htoaa/CMSSW_15_0_10/src/PhysicsTools/NanoTuples


#Let's load the files we want to analyze.
def make_root_file_vector(file_list):
    files_vec = ROOT.std.vector("string")()

    for entry in file_list:
        files_vec.push_back(str(entry))

    return files_vec

#This should help us when a root file is bad/doesnt contain our desired variables. (Example QCD0B has no 'Events' in TTree).
def file_has_tree(filename, tree_name="Events"):
    f = ROOT.TFile.Open(str(filename), "READ")

    if not f or f.IsZombie():
        return False

    obj = f.Get(tree_name)
    ok = bool(obj) and obj.InheritsFrom("TTree")

    f.Close()
    return ok


#This is how we'll read in our datasets.
def get_files_for_sample(parent_dir, sample_name, sample_info, max_files=None, log_dir="logs"):
    sample_dir = parent_dir / sample_info["subdir"]

    if not sample_dir.is_dir():
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        with open(log_dir / "missing_sample_dirs.txt", "a") as out:
            out.write(f"{sample_name}: {sample_dir}\n")

        return []

    all_files = sorted(sample_dir.glob(sample_info["pattern"]))

    if max_files is not None:
        all_files = all_files[:max_files]

    good_files = []
    bad_files = []

    for f in all_files:
        if file_has_tree(f, "Events"):
            good_files.append(str(f))
        else:
            bad_files.append(str(f))

    if bad_files:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        bad_file_log = log_dir / f"bad_files_{sample_name}.txt"

        with open(bad_file_log, "w") as out:
            for bad in bad_files:
                out.write(bad + "\n")

        print(f"Warning: {sample_name} has bad/missing-Events files. See {bad_file_log}")

    
    return good_files


#Make one RDataFrame per sample.
sample_files = {}
sample_rdf = {}

for sample_name, info in samples_to_run.items():
    files = get_files_for_sample(input_dir, sample_name, info, max_files=args.max_files, log_dir="logs")

    sample_files[sample_name] = files

    if len(files) == 0:
        continue

    files_vec = make_root_file_vector(files)

    sample_rdf[sample_name] = ROOT.RDataFrame("Events", files_vec)


#-----------------------------------------------------------------------------#Legacy File Load (Single File)------------------------------------------------------------------------------#


"""
# Load NanoAOD file
rdf = ROOT.RDataFrame("Events", "/cms/data/store/mc/RunIII2024Summer24NanoAODv15/GluGluH-01J-HToAATo4B_Par-M-35_TuneCP5_13p6TeV_madgraph-pythia8/NANOAODSIM/150X_mcRun3_2024_realistic_v2-v2/2520000/0afb91ad-bf79-4830-ba1a-ebb5b2a0b4b4.root")
"""


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
'''
# 1. Define a mask for GenParticles that are electrons (pdgId 11)
# GenPart_pdgId is a vector branch, Define applies this per-event
rdf_with_mask = rdf.Define("GenElecMask", "abs(GenPart_pdgId) == 11")

# 2. Filter events: Keep only events where ANY electron passes the mask
rdf_filtered = rdf_with_mask.Filter("ROOT::VecOps::Any(GenElecMask)")

# 3. (Optional) Filter by pT: Keep events with electrons > 20 GeV
rdf_final = rdf_filtered.Filter("ROOT::VecOps::Any(GenPart_pt[GenElecMask] > 20)")
'''

#-------------------------------------------------------------------------------#Gen-Level Module------------------------------------------------------------------------------------------#
#We Define Gen-Level variables and process them in this block.

"""
#Define a Mask for Higgs (pdgId == 25) for GenParticles. Include the pt cut here (pt > 1)
rdf = rdf.Define("GenHiggsMask", "GenPart_pdgId == 25")\
         .Define("Higgs_Gen_pt", "GenPart_pt[GenHiggsMask]")\
         .Define("Higgs_Gen_phi", "GenPart_phi[GenHiggsMask]")\
         .Define("Higgs_Gen_eta", "GenPart_eta[GenHiggsMask]")\
         .Define("Higgs_Gen_mass", "GenPart_mass[GenHiggsMask]")\
         .Define("Higgs_Gen_status", "GenPart_status[GenHiggsMask]")

#Define the isFirst Mask (status == 22)
rdf = rdf.Define("isFirst", "Higgs_Gen_status == 22")\
         .Define("Higgs_GenFirst_pt", "Higgs_Gen_pt[isFirst]")\
         .Define("Higgs_GenFirst_phi", "Higgs_Gen_phi[isFirst]")\
         .Define("Higgs_GenFirst_eta", "Higgs_Gen_eta[isFirst]")\
         .Define("Higgs_GenFirst_mass", "Higgs_Gen_mass[isFirst]")

#Define the isLast Mask (status == 62)
rdf = rdf.Define("isLast", "Higgs_Gen_status == 62")\
         .Define("Higgs_GenLast_pt", "Higgs_Gen_pt[isLast]")\
         .Define("Higgs_GenLast_phi", "Higgs_Gen_phi[isLast]")\
         .Define("Higgs_GenLast_eta", "Higgs_Gen_eta[isLast]")\
         .Define("Higgs_GenLast_mass", "Higgs_Gen_mass[isLast]")
"""



#-----------------------------------------------------------------------------#Particle Transformer Module---------------------------------------------------------------------------------#

#Particle Transformer Module. We'll define ParT2 and ParT3 variables here. 


#Declare a helper function in case FatJet_genAK8Idx is a different length than GenJetAK8_nBHadrons.
ROOT.gInterpreter.Declare("""
#include "ROOT/RVec.hxx"
#include <cstddef>

ROOT::RVec<std::size_t> get0bFatJetIdx(const ROOT::RVecI& FatJet_genJetAK8Idx,
                                       const ROOT::RVecI& GenJetAK8_nBHadrons) {
    ROOT::RVec<std::size_t> idxs;

    for (std::size_t i = 0; i < FatJet_genJetAK8Idx.size(); ++i) {
        int genIdx = FatJet_genJetAK8Idx[i];

        if (genIdx >= 0 &&
            static_cast<std::size_t>(genIdx) < GenJetAK8_nBHadrons.size() &&
            GenJetAK8_nBHadrons[genIdx] >= 0) {
            idxs.push_back(i);
        }
    }

    return idxs;
}
""")

ROOT.gInterpreter.Declare("""
#include "ROOT/RVec.hxx"
#include <cstddef>

ROOT::RVec<std::size_t> get1bFatJetIdx(const ROOT::RVecI& FatJet_genJetAK8Idx,
                                       const ROOT::RVecI& GenJetAK8_nBHadrons) {
    ROOT::RVec<std::size_t> idxs;

    for (std::size_t i = 0; i < FatJet_genJetAK8Idx.size(); ++i) {
        int genIdx = FatJet_genJetAK8Idx[i];

        if (genIdx >= 0 &&
            static_cast<std::size_t>(genIdx) < GenJetAK8_nBHadrons.size() &&
            GenJetAK8_nBHadrons[genIdx] >= 1) {
            idxs.push_back(i);
        }
    }

    return idxs;
}
""")

ROOT.gInterpreter.Declare("""
#include "ROOT/RVec.hxx"
#include <cstddef>

ROOT::RVec<std::size_t> get2bFatJetIdx(const ROOT::RVecI& FatJet_genJetAK8Idx,
                                       const ROOT::RVecI& GenJetAK8_nBHadrons) {
    ROOT::RVec<std::size_t> idxs;

    for (std::size_t i = 0; i < FatJet_genJetAK8Idx.size(); ++i) {
        int genIdx = FatJet_genJetAK8Idx[i];

        if (genIdx >= 0 &&
            static_cast<std::size_t>(genIdx) < GenJetAK8_nBHadrons.size() &&
            GenJetAK8_nBHadrons[genIdx] >= 2) {
            idxs.push_back(i);
        }
    }

    return idxs;
}
""")

ROOT.gInterpreter.Declare("""
#include "ROOT/RVec.hxx"
#include <cstddef>

ROOT::RVec<std::size_t> get3bFatJetIdx(const ROOT::RVecI& FatJet_genJetAK8Idx,
                                       const ROOT::RVecI& GenJetAK8_nBHadrons) {
    ROOT::RVec<std::size_t> idxs;

    for (std::size_t i = 0; i < FatJet_genJetAK8Idx.size(); ++i) {
        int genIdx = FatJet_genJetAK8Idx[i];

        if (genIdx >= 0 &&
            static_cast<std::size_t>(genIdx) < GenJetAK8_nBHadrons.size() &&
            GenJetAK8_nBHadrons[genIdx] >= 3) {
            idxs.push_back(i);
        }
    }

    return idxs;
}
""")

ROOT.gInterpreter.Declare("""
#include "ROOT/RVec.hxx"
#include <cstddef>

ROOT::RVec<std::size_t> get4bFatJetIdx(const ROOT::RVecI& FatJet_genJetAK8Idx,
                                       const ROOT::RVecI& GenJetAK8_nBHadrons) {
    ROOT::RVec<std::size_t> idxs;

    for (std::size_t i = 0; i < FatJet_genJetAK8Idx.size(); ++i) {
        int genIdx = FatJet_genJetAK8Idx[i];

        if (genIdx >= 0 &&
            static_cast<std::size_t>(genIdx) < GenJetAK8_nBHadrons.size() &&
            GenJetAK8_nBHadrons[genIdx] >= 4) {
            idxs.push_back(i);
        }
    }

    return idxs;
}
""")


#Let's set up a mask to make sure we only investigate events with some tagger score in the desired final state. "FatJet_pt > 300" getHas4bScoreMask(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons)")
def define_ParT_variables(rdf):

    #Define varibles with no cuts applied. 
    #Define FatJet kinematics
    rdf = rdf.Define("FatJet_pt_full", "FatJet_pt")\
             .Define("FatJet_eta_full", "FatJet_eta")\
             .Define("FatJet_msoftdrop_full", "FatJet_msoftdrop")
    #Define FatJet Tagger Scores for on-shell ParT2 variables.
    rdf = rdf.Define("FatJet_ParT2_3b_full", "FatJet_globalParT2_probHZxZxbbb")\
             .Define("FatJet_ParT2_4b_full", "FatJet_globalParT2_probHZxZxbbbb")\
             .Define("FatJet_ParT2_b_channels_full","FatJet_ParT2_3b_full + FatJet_ParT2_4b_full")\
             .Define("FatJet_ParT2_QCD_full", "FatJet_globalParT2_probQCDb + FatJet_globalParT2_probQCDbb + FatJet_globalParT2_probQCDc + FatJet_globalParT2_probQCDcc + FatJet_globalParT2_probQCDothers")\
             .Define("FatJet_ParT2_3b_full_Normed", "FatJet_ParT2_3b_full /(FatJet_ParT2_3b_full +  FatJet_ParT2_QCD_full)")\
             .Define("FatJet_ParT2_4b_full_Normed", "FatJet_ParT2_4b_full /(FatJet_ParT2_4b_full +  FatJet_ParT2_QCD_full)")\
             .Define("FatJet_ParT2_b_channels_full_Normed","FatJet_ParT2_b_channels_full / (FatJet_ParT2_b_channels_full + FatJet_ParT2_QCD_full)")
    #Define FatJet Tagger Scores for on-shell ParT3 variables.
    rdf = rdf.Define("FatJet_ParT3_3b_full", "FatJet_globalParT3_probRawHZxZxbbb")\
             .Define("FatJet_ParT3_4b_full", "FatJet_globalParT3_probRawHZxZxbbbb")\
             .Define("FatJet_ParT3_b_channels_full","FatJet_ParT3_3b_full + FatJet_ParT3_4b_full")\
             .Define("FatJet_ParT3_QCD_full", "FatJet_globalParT3_QCD")\
             .Define("FatJet_ParT3_3b_full_Normed", "FatJet_ParT3_3b_full /(FatJet_ParT3_3b_full +  FatJet_ParT3_QCD_full)")\
             .Define("FatJet_ParT3_4b_full_Normed", "FatJet_ParT3_4b_full /(FatJet_ParT3_4b_full +  FatJet_ParT3_QCD_full)")\
             .Define("FatJet_ParT3_b_channels_full_Normed","FatJet_ParT3_b_channels_full / (FatJet_ParT3_b_channels_full + FatJet_ParT3_QCD_full)")



    #Define varibales with nbHad = 0 cut.
    rdf = rdf.Define("FatJet_0b_idx", "get0bFatJetIdx(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons)") 
    #Define FatJet kinematics
    rdf = rdf.Define("FatJet_0b_pt", "Take(FatJet_pt, FatJet_0b_idx)")\
             .Define("FatJet_0b_eta", "Take(FatJet_eta, FatJet_0b_idx)")\
             .Define("FatJet_0b_msoftdrop", "Take(FatJet_msoftdrop, FatJet_0b_idx)")
    #Define FatJet Tagger Scores for on-shell ParT2 variables.
    rdf = rdf.Define("FatJet_0b_ParT2_3b", "Take(FatJet_globalParT2_probHZxZxbbb, FatJet_0b_idx)")\
             .Define("FatJet_0b_ParT2_4b", "Take(FatJet_globalParT2_probHZxZxbbbb, FatJet_0b_idx)")\
             .Define("FatJet_0b_ParT2_b_channels","FatJet_0b_ParT2_3b + FatJet_0b_ParT2_4b")\
             .Define("FatJet_0b_ParT2_QCD", "Take(FatJet_globalParT2_probQCDb, FatJet_0b_idx) + Take(FatJet_globalParT2_probQCDbb, FatJet_0b_idx) + Take(FatJet_globalParT2_probQCDc, FatJet_0b_idx) + Take(FatJet_globalParT2_probQCDcc, FatJet_0b_idx) + Take(FatJet_globalParT2_probQCDothers, FatJet_0b_idx)")\
             .Define("FatJet_0b_ParT2_3b_Normed", "FatJet_0b_ParT2_3b /(FatJet_0b_ParT2_3b +  FatJet_0b_ParT2_QCD)")\
             .Define("FatJet_0b_ParT2_4b_Normed", "FatJet_0b_ParT2_4b /(FatJet_0b_ParT2_4b +  FatJet_0b_ParT2_QCD)")\
             .Define("FatJet_0b_ParT2_b_channels_Normed","FatJet_0b_ParT2_b_channels / (FatJet_0b_ParT2_b_channels + FatJet_0b_ParT2_QCD)")    
    #Define FatJet Tagger Scores for on-shell ParT3 variables.         
    rdf = rdf.Define("FatJet_0b_ParT3_3b", "Take(FatJet_globalParT3_probRawHZxZxbbb, FatJet_0b_idx)")\
             .Define("FatJet_0b_ParT3_4b", "Take(FatJet_globalParT3_probRawHZxZxbbbb, FatJet_0b_idx)")\
             .Define("FatJet_0b_ParT3_b_channels","FatJet_0b_ParT3_3b + FatJet_0b_ParT3_4b")\
             .Define("FatJet_0b_ParT3_QCD", "Take(FatJet_globalParT3_QCD, FatJet_0b_idx)")\
             .Define("FatJet_0b_ParT3_3b_Normed", "FatJet_0b_ParT3_3b /(FatJet_0b_ParT3_3b +  FatJet_0b_ParT3_QCD)")\
             .Define("FatJet_0b_ParT3_4b_Normed", "FatJet_0b_ParT3_4b /(FatJet_0b_ParT3_4b +  FatJet_0b_ParT3_QCD)")\
             .Define("FatJet_0b_ParT3_b_channels_Normed","FatJet_0b_ParT3_b_channels / (FatJet_0b_ParT3_b_channels + FatJet_0b_ParT3_QCD)")

    
    #Define varibales with nbHad = 1 cut.
    rdf = rdf.Define("FatJet_1b_idx", "get1bFatJetIdx(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons)")
    #Define FatJet kinematics
    rdf = rdf.Define("FatJet_1b_pt", "Take(FatJet_pt, FatJet_1b_idx)")\
             .Define("FatJet_1b_eta", "Take(FatJet_eta, FatJet_1b_idx)")\
             .Define("FatJet_1b_msoftdrop", "Take(FatJet_msoftdrop, FatJet_1b_idx)")
    #Define FatJet Tagger Scores for on-shell ParT2 variables.
    rdf = rdf.Define("FatJet_1b_ParT2_3b", "Take(FatJet_globalParT2_probHZxZxbbb, FatJet_1b_idx)")\
             .Define("FatJet_1b_ParT2_4b", "Take(FatJet_globalParT2_probHZxZxbbbb, FatJet_1b_idx)")\
             .Define("FatJet_1b_ParT2_b_channels","FatJet_1b_ParT2_3b + FatJet_1b_ParT2_4b")\
             .Define("FatJet_1b_ParT2_QCD", "Take(FatJet_globalParT2_probQCDb, FatJet_1b_idx) + Take(FatJet_globalParT2_probQCDbb, FatJet_1b_idx) + Take(FatJet_globalParT2_probQCDc, FatJet_1b_idx) + Take(FatJet_globalParT2_probQCDcc, FatJet_1b_idx) + Take(FatJet_globalParT2_probQCDothers, FatJet_1b_idx)")\
             .Define("FatJet_1b_ParT2_3b_Normed", "FatJet_1b_ParT2_3b /(FatJet_1b_ParT2_3b +  FatJet_1b_ParT2_QCD)")\
             .Define("FatJet_1b_ParT2_4b_Normed", "FatJet_1b_ParT2_4b /(FatJet_1b_ParT2_4b +  FatJet_1b_ParT2_QCD)")\
             .Define("FatJet_1b_ParT2_b_channels_Normed","FatJet_1b_ParT2_b_channels / (FatJet_1b_ParT2_b_channels + FatJet_1b_ParT2_QCD)")
    #Define FatJet Tagger Scores for on-shell ParT3 variables.         
    rdf = rdf.Define("FatJet_1b_ParT3_3b", "Take(FatJet_globalParT3_probRawHZxZxbbb, FatJet_1b_idx)")\
             .Define("FatJet_1b_ParT3_4b", "Take(FatJet_globalParT3_probRawHZxZxbbbb, FatJet_1b_idx)")\
             .Define("FatJet_1b_ParT3_b_channels","FatJet_1b_ParT3_3b + FatJet_1b_ParT3_4b")\
             .Define("FatJet_1b_ParT3_QCD", "Take(FatJet_globalParT3_QCD, FatJet_1b_idx)")\
             .Define("FatJet_1b_ParT3_3b_Normed", "FatJet_1b_ParT3_3b /(FatJet_1b_ParT3_3b +  FatJet_1b_ParT3_QCD)")\
             .Define("FatJet_1b_ParT3_4b_Normed", "FatJet_1b_ParT3_4b /(FatJet_1b_ParT3_4b +  FatJet_1b_ParT3_QCD)")\
             .Define("FatJet_1b_ParT3_b_channels_Normed","FatJet_1b_ParT3_b_channels / (FatJet_1b_ParT3_b_channels + FatJet_1b_ParT3_QCD)")

    
    #Define varibales with nbHad = 2 cut.
    rdf = rdf.Define("FatJet_2b_idx", "get2bFatJetIdx(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons)")
    #Define FatJet kinematics
    rdf = rdf.Define("FatJet_2b_pt", "Take(FatJet_pt, FatJet_2b_idx)")\
             .Define("FatJet_2b_eta", "Take(FatJet_eta, FatJet_2b_idx)")\
             .Define("FatJet_2b_msoftdrop", "Take(FatJet_msoftdrop, FatJet_2b_idx)")
    #Define FatJet Tagger Scores for on-shell ParT2 variables.
    rdf = rdf.Define("FatJet_2b_ParT2_3b", "Take(FatJet_globalParT2_probHZxZxbbb, FatJet_2b_idx)")\
             .Define("FatJet_2b_ParT2_4b", "Take(FatJet_globalParT2_probHZxZxbbbb, FatJet_2b_idx)")\
             .Define("FatJet_2b_ParT2_b_channels","FatJet_2b_ParT2_3b + FatJet_2b_ParT2_4b")\
             .Define("FatJet_2b_ParT2_QCD", "Take(FatJet_globalParT2_probQCDb, FatJet_2b_idx) + Take(FatJet_globalParT2_probQCDbb, FatJet_2b_idx) + Take(FatJet_globalParT2_probQCDc, FatJet_2b_idx) + Take(FatJet_globalParT2_probQCDcc, FatJet_2b_idx) + Take(FatJet_globalParT2_probQCDothers, FatJet_2b_idx)")\
             .Define("FatJet_2b_ParT2_3b_Normed", "FatJet_2b_ParT2_3b /(FatJet_2b_ParT2_3b +  FatJet_2b_ParT2_QCD)")\
             .Define("FatJet_2b_ParT2_4b_Normed", "FatJet_2b_ParT2_4b /(FatJet_2b_ParT2_4b +  FatJet_2b_ParT2_QCD)")\
             .Define("FatJet_2b_ParT2_b_channels_Normed","FatJet_2b_ParT2_b_channels / (FatJet_2b_ParT2_b_channels + FatJet_2b_ParT2_QCD)")
    #Define FatJet Tagger Scores for on-shell ParT3 variables.
    rdf = rdf.Define("FatJet_2b_ParT3_3b", "Take(FatJet_globalParT3_probRawHZxZxbbb, FatJet_2b_idx)")\
             .Define("FatJet_2b_ParT3_4b", "Take(FatJet_globalParT3_probRawHZxZxbbbb, FatJet_2b_idx)")\
             .Define("FatJet_2b_ParT3_b_channels","FatJet_2b_ParT3_3b + FatJet_2b_ParT3_4b")\
             .Define("FatJet_2b_ParT3_QCD", "Take(FatJet_globalParT3_QCD, FatJet_2b_idx)")\
             .Define("FatJet_2b_ParT3_3b_Normed", "FatJet_2b_ParT3_3b /(FatJet_2b_ParT3_3b +  FatJet_2b_ParT3_QCD)")\
             .Define("FatJet_2b_ParT3_4b_Normed", "FatJet_2b_ParT3_4b /(FatJet_2b_ParT3_4b +  FatJet_2b_ParT3_QCD)")\
             .Define("FatJet_2b_ParT3_b_channels_Normed","FatJet_2b_ParT3_b_channels / (FatJet_2b_ParT3_b_channels + FatJet_2b_ParT3_QCD)")


    #Define varibales with nbHad = 3 cut.
    rdf = rdf.Define("FatJet_3b_idx", "get3bFatJetIdx(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons)")
    #Define FatJet kinematics
    rdf = rdf.Define("FatJet_3b_pt", "Take(FatJet_pt, FatJet_3b_idx)")\
             .Define("FatJet_3b_eta", "Take(FatJet_eta, FatJet_3b_idx)")\
             .Define("FatJet_3b_msoftdrop", "Take(FatJet_msoftdrop, FatJet_3b_idx)")
    #Define FatJet Tagger Scores for on-shell ParT2 variables.
    rdf = rdf.Define("FatJet_3b_ParT2_3b", "Take(FatJet_globalParT2_probHZxZxbbb, FatJet_3b_idx)")\
             .Define("FatJet_3b_ParT2_4b", "Take(FatJet_globalParT2_probHZxZxbbbb, FatJet_3b_idx)")\
             .Define("FatJet_3b_ParT2_b_channels","FatJet_3b_ParT2_3b + FatJet_3b_ParT2_4b")\
             .Define("FatJet_3b_ParT2_QCD", "Take(FatJet_globalParT2_probQCDb, FatJet_3b_idx) + Take(FatJet_globalParT2_probQCDbb, FatJet_3b_idx) + Take(FatJet_globalParT2_probQCDc, FatJet_3b_idx) + Take(FatJet_globalParT2_probQCDcc, FatJet_3b_idx) + Take(FatJet_globalParT2_probQCDothers, FatJet_3b_idx)")\
             .Define("FatJet_3b_ParT2_3b_Normed", "FatJet_3b_ParT2_3b /(FatJet_3b_ParT2_3b +  FatJet_3b_ParT2_QCD)")\
             .Define("FatJet_3b_ParT2_4b_Normed", "FatJet_3b_ParT2_4b /(FatJet_3b_ParT2_4b +  FatJet_3b_ParT2_QCD)")\
             .Define("FatJet_3b_ParT2_b_channels_Normed","FatJet_3b_ParT2_b_channels / (FatJet_3b_ParT2_b_channels + FatJet_3b_ParT2_QCD)")
    #Define FatJet Tagger Scores for on-shell ParT3 variables.
    rdf = rdf.Define("FatJet_3b_ParT3_3b", "Take(FatJet_globalParT3_probRawHZxZxbbb, FatJet_3b_idx)")\
             .Define("FatJet_3b_ParT3_4b", "Take(FatJet_globalParT3_probRawHZxZxbbbb, FatJet_3b_idx)")\
             .Define("FatJet_3b_ParT3_b_channels","FatJet_3b_ParT3_3b + FatJet_3b_ParT3_4b")\
             .Define("FatJet_3b_ParT3_QCD", "Take(FatJet_globalParT3_QCD, FatJet_3b_idx)")\
             .Define("FatJet_3b_ParT3_3b_Normed", "FatJet_3b_ParT3_3b /(FatJet_3b_ParT3_3b +  FatJet_3b_ParT3_QCD)")\
             .Define("FatJet_3b_ParT3_4b_Normed", "FatJet_3b_ParT3_4b /(FatJet_3b_ParT3_4b +  FatJet_3b_ParT3_QCD)")\
             .Define("FatJet_3b_ParT3_b_channels_Normed","FatJet_3b_ParT3_b_channels / (FatJet_3b_ParT3_b_channels + FatJet_3b_ParT3_QCD)")

    
    #Define varibales with nbHad = 4 cut.
    rdf = rdf.Define("FatJet_4b_idx", "get4bFatJetIdx(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons)")
    #Define FatJet kinematics
    rdf = rdf.Define("FatJet_4b_pt", "Take(FatJet_pt, FatJet_4b_idx)")\
             .Define("FatJet_4b_eta", "Take(FatJet_eta, FatJet_4b_idx)")\
             .Define("FatJet_4b_msoftdrop", "Take(FatJet_msoftdrop, FatJet_4b_idx)")
    #Define FatJet Tagger Scores for on-shell ParT2 variables.
    rdf = rdf.Define("FatJet_4b_ParT2_3b", "Take(FatJet_globalParT2_probHZxZxbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT2_4b", "Take(FatJet_globalParT2_probHZxZxbbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT2_b_channels","FatJet_4b_ParT2_3b + FatJet_4b_ParT2_4b")\
             .Define("FatJet_4b_ParT2_QCD", "Take(FatJet_globalParT2_probQCDb, FatJet_4b_idx) + Take(FatJet_globalParT2_probQCDbb, FatJet_4b_idx) + Take(FatJet_globalParT2_probQCDc, FatJet_4b_idx) + Take(FatJet_globalParT2_probQCDcc, FatJet_4b_idx) + Take(FatJet_globalParT2_probQCDothers, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT2_3b_Normed", "FatJet_4b_ParT2_3b /(FatJet_4b_ParT2_3b +  FatJet_4b_ParT2_QCD)")\
             .Define("FatJet_4b_ParT2_4b_Normed", "FatJet_4b_ParT2_4b /(FatJet_4b_ParT2_4b +  FatJet_4b_ParT2_QCD)")\
             .Define("FatJet_4b_ParT2_b_channels_Normed","FatJet_4b_ParT2_b_channels / (FatJet_4b_ParT2_b_channels + FatJet_4b_ParT2_QCD)")
    #Define FatJet Tagger Scores for on-shell ParT3 variables.
    rdf = rdf.Define("FatJet_4b_ParT3_3b", "Take(FatJet_globalParT3_probRawHZxZxbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT3_4b", "Take(FatJet_globalParT3_probRawHZxZxbbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT3_b_channels","FatJet_4b_ParT3_3b + FatJet_4b_ParT3_4b")\
             .Define("FatJet_4b_ParT3_QCD", "Take(FatJet_globalParT3_QCD, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT3_3b_Normed", "FatJet_4b_ParT3_3b /(FatJet_4b_ParT3_3b +  FatJet_4b_ParT3_QCD)")\
             .Define("FatJet_4b_ParT3_4b_Normed", "FatJet_4b_ParT3_4b /(FatJet_4b_ParT3_4b +  FatJet_4b_ParT3_QCD)")\
             .Define("FatJet_4b_ParT3_b_channels_Normed","FatJet_4b_ParT3_b_channels / (FatJet_4b_ParT3_b_channels + FatJet_4b_ParT3_QCD)")


    """
    #Define FatJet Tagger Scores for including off-shell ParT2 variables.
    rdf = rdf.Define("FatJet_4b_ParT2_3b_adv1", "Take(FatJet_globalParT2_probHZxZxStarbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT2_4b_adv1", "Take(FatJet_globalParT2_probHZxZxStarbbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT2_b_channels_adv1","FatJet_4b_ParT2_3b_adv1 + FatJet_4b_ParT2_4b_adv1")\
             .Define("FatJet_4b_ParT2_3b_adv1_Normed", "FatJet_4b_ParT2_3b_adv1 /(FatJet_4b_ParT2_3b_adv1 +  FatJet_4b_ParT2_QCD)")\
             .Define("FatJet_4b_ParT2_4b_adv1_Normed", "FatJet_4b_ParT2_4b_adv1 /(FatJet_4b_ParT2_4b_adv1 +  FatJet_4b_ParT2_QCD)")\
             .Define("FatJet_4b_ParT2_b_channels_adv1_Normed","FatJet_4b_ParT2_b_channels / (FatJet_4b_ParT2_b_channels_adv1 + FatJet_4b_ParT2_QCD)")\
             .Define("FatJet_4b_ParT2_3b_adv2", "Take(FatJet_globalParT2_probHZZbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT2_4b_adv2", "Take(FatJet_globalParT2_probHZZbbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT2_b_channels_adv2","FatJet_4b_ParT2_3b_adv2 + FatJet_4b_ParT2_4b_adv2")\
             .Define("FatJet_4b_ParT2_3b_adv2_Normed", "FatJet_4b_ParT2_3b_adv2 /(FatJet_4b_ParT2_3b_adv2 +  FatJet_4b_ParT2_QCD)")\
             .Define("FatJet_4b_ParT2_4b_adv2_Normed", "FatJet_4b_ParT2_4b_adv2 /(FatJet_4b_ParT2_4b_adv2 +  FatJet_4b_ParT2_QCD)")\
             .Define("FatJet_4b_ParT2_b_channels_adv2_Normed","FatJet_4b_ParT2_b_channels_adv2 / (FatJet_4b_ParT2_b_channels_adv2 + FatJet_4b_ParT2_QCD)")
         

    #Define FatJet Tagger Scores for including off-shell ParT3 variables.
    rdf = rdf.Define("FatJet_4b_ParT3_3b_adv1", "Take(FatJet_globalParT3_probRawHZxZxStarbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT3_4b_adv1", "Take(FatJet_globalParT3_probRawHZxZxStarbbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT3_b_channels_adv1","FatJet_4b_ParT3_3b_adv1 + FatJet_4b_ParT3_4b_adv1")\
             .Define("FatJet_4b_ParT3_3b_adv1_Normed", "FatJet_4b_ParT3_3b_adv1 /(FatJet_4b_ParT3_3b_adv1 +  FatJet_4b_ParT3_QCD)")\
             .Define("FatJet_4b_ParT3_4b_adv1_Normed", "FatJet_4b_ParT3_4b_adv1 /(FatJet_4b_ParT3_4b_adv1 +  FatJet_4b_ParT3_QCD)")\
             .Define("FatJet_4b_ParT3_b_channels_adv1_Normed","FatJet_4b_ParT3_b_channels / (FatJet_4b_ParT3_b_channels_adv1 + FatJet_4b_ParT3_QCD)")\
             .Define("FatJet_4b_ParT3_3b_adv2", "Take(FatJet_globalParT3_probRawHZZbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT3_4b_adv2", "Take(FatJet_globalParT3_probRawHZZbbbb, FatJet_4b_idx)")\
             .Define("FatJet_4b_ParT3_b_channels_adv2","FatJet_4b_ParT3_3b_adv2 + FatJet_4b_ParT3_4b_adv2")\
             .Define("FatJet_4b_ParT3_3b_adv2_Normed", "FatJet_4b_ParT3_3b_adv2 /(FatJet_4b_ParT3_3b_adv2 +  FatJet_4b_ParT3_QCD)")\
             .Define("FatJet_4b_ParT3_4b_adv2_Normed", "FatJet_4b_ParT3_4b_adv2 /(FatJet_4b_ParT3_4b_adv2 +  FatJet_4b_ParT3_QCD)")\
             .Define("FatJet_4b_ParT3_b_channels_adv2_Normed","FatJet_4b_ParT3_b_channels_adv2 / (FatJet_4b_ParT3_b_channels_adv2 + FatJet_4b_ParT3_QCD)")
    """
    return rdf


#Now we're ready to generate multiple RDataFrames
rdf_defined = {}

for sample_name, rdf in sample_rdf.items():
    rdf_defined[sample_name] = define_ParT_variables(rdf)


#---------------------------------------------------------------------------------#Mismatch Debug------------------------------------------------------------------------------------------#
#Define the debugger to find the mismatch between isFirst pt and isLast pt.
"""
rdf_debug = (
    rdf
    .Define("n_Higgs_GenFirst_pt", "Higgs_GenFirst_pt.size()")
    .Define("n_Higgs_GenLast_pt",  "Higgs_GenLast_pt.size()")
)

print("Mismatch count:",
      rdf_debug.Filter("n_Higgs_GenFirst_pt != n_Higgs_GenLast_pt").Count().GetValue())

rdf_debug.Filter("n_Higgs_GenFirst_pt != n_Higgs_GenLast_pt") \
    .Display(
        ["n_Higgs_GenFirst_pt", "n_Higgs_GenLast_pt",
         "Higgs_GenFirst_pt", "Higgs_GenLast_pt"],
        10
    ).Print()



columns = ["GenPart_pdgId","GenPart_status","GenPart_genPartIdxMother",
             "Higgs_GenFirst_pt","Higgs_GenFirst_phi","Higgs_GenFirst_eta","Higgs_GenFirst_mass","Higgs_GenLast_pt","Higgs_GenLast_phi","Higgs_GenLast_eta","Higgs_GenLast_mass"]

display = rdf.Display(columns,10)
#print(display.AsString())


#Apply Higgs Mask
#rdf_H_filtered = rdf_Higgs_Mask.Filter("ROOT::VecOps::Any(GenHiggsMask)")
"""



#---------------------------------------------------------------------------#Gen-Level Histogram Module------------------------------------------------------------------------------------#
"""
#Generate Gen-Level kinematic histograms
#Gen-Level First
h_Higgs_GenFirst_pt = rdf.Histo1D(("Higgs_GenFirst_pt", "Higgs Gen First Pt; p_{T} [GeV]; Events", 50, 0., 500), "Higgs_GenFirst_pt")
h_Higgs_GenFirst_phi = rdf.Histo1D(("Higgs_GenFirst_phi", "Higgs Gen First #phi; #phi; Events", 50, -3.2, 3.2), "Higgs_GenFirst_phi")
h_Higgs_GenFirst_eta = rdf.Histo1D(("Higgs_GenFirst_eta", "Higgs Gen First #eta; #eta; Events", 50, -7., 7.), "Higgs_GenFirst_eta")
h_Higgs_GenFirst_mass = rdf.Histo1D(("Higgs_GenFirst_mass", "Higgs Gen First Mass; Mass [GeV]; Events", 50, 124., 126.), "Higgs_GenFirst_mass")
#Gen-Level Last
h_Higgs_GenLast_pt = rdf.Histo1D(("Higgs_GenLast_pt", "Higgs Gen Last Pt; p_{T} [GeV]; Events", 50, 0., 500), "Higgs_GenLast_pt")
h_Higgs_GenLast_phi = rdf.Histo1D(("Higgs_GenLast_phi", "Higgs Gen Last #phi; #phi; Events", 50, -3.2, 3.2), "Higgs_GenLast_phi")
h_Higgs_GenLast_eta = rdf.Histo1D(("Higgs_GenLast_eta", "Higgs Gen Last #eta; #eta; Events", 50, -7., 7.), "Higgs_GenLast_eta")
h_Higgs_GenLast_mass = rdf.Histo1D(("Higgs_GenLast_mass", "Higgs Gen Last Mass; Mass [GeV]; Events", 50, 124., 126.), "Higgs_GenLast_mass")
#Gen-Level 2D
h2_HiggsPt_GenFirst_GenLast = rdf.Histo2D(("Higgs_GenFirst_GenLast_pt", "Higgs Pt Gen First v Gen Last; Gen First p_{T} [GeV]; Gen Last p_{T} [GeV]", 100, 0., 1000., 100, 0., 1000.), "Higgs_GenFirst_pt", "Higgs_GenLast_pt")



#Draw kinematic histograms
#Gen-Level First
h_Higgs_GenFirst_pt.Draw()
h_Higgs_GenFirst_phi.Draw()
h_Higgs_GenFirst_eta.Draw()
h_Higgs_GenFirst_mass.Draw()
#Gen-Level Last
h_Higgs_GenLast_pt.Draw()
h_Higgs_GenLast_phi.Draw()
h_Higgs_GenLast_eta.Draw()
h_Higgs_GenLast_mass.Draw()
#Gen-Level 2D
h2_HiggsPt_GenFirst_GenLast.Draw()
"""
#---------------------------------------------------------------------------------------------------------#FatJet Histogram Module-------------------------------------------------------------------------------------------------------------------#
#We'll define our FatJet histograms here.

def book_histograms(rdf, sample_name, label):
    histos = {}
    
    #Full uncut histograms
    #Kinematics
    histos["pt"] = rdf.Histo1D((f"h_{sample_name}_FatJet_pt", f"{label};FatJet p_{{T}} [GeV];Events", 100, 100., 1000.), "FatJet_pt_full")
    histos["eta"] = rdf.Histo1D((f"h_{sample_name}_FatJet_eta", f"{label};FatJet #eta;Events", 100, -7., 7.), "FatJet_eta_full")
    histos["msoftdrop"] = rdf.Histo1D((f"h_{sample_name}_FatJet_msoftdrop", f"{label};Soft drop mass [GeV];Events", 100, 20., 120.), "FatJet_msoftdrop_full")
    #On-Shell Tagger Scores
    histos["ParT2_3b"] = rdf.Histo1D((f"h_{sample_name}_ParT2_3b", f"{label};ParT2 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_ParT2_3b_full_Normed")
    histos["ParT2_4b"] = rdf.Histo1D((f"h_{sample_name}_ParT2_4b", f"{label};ParT2 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_ParT2_4b_full_Normed")
    histos["ParT2_b_channels"] = rdf.Histo1D((f"h_{sample_name}_ParT2_b_channels", f"{label};ParT2 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_ParT2_b_channels_full_Normed")
    histos["ParT3_3b"] = rdf.Histo1D((f"h_{sample_name}_ParT3_3b", f"{label};ParT3 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_ParT3_3b_full_Normed")
    histos["ParT3_4b"] = rdf.Histo1D((f"h_{sample_name}_ParT3_4b", f"{label};ParT3 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_ParT3_4b_full_Normed")
    histos["ParT3_b_channels"] = rdf.Histo1D((f"h_{sample_name}_ParT3_b_channels", f"{label};ParT3 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_ParT3_b_channels_full_Normed")

    
    #Selection-Cut Histograms

    #nBHad >= 0
    #Kinematics
    histos["0b_pt"] = rdf.Histo1D((f"h_{sample_name}_FatJet_0b_pt", f"{label} (nBHad >= 0);FatJet p_{{T}} [GeV];Events", 100, 100., 1000.), "FatJet_0b_pt")
    histos["0b_eta"] = rdf.Histo1D((f"h_{sample_name}_FatJet_0b_eta", f"{label} (nBHad >= 0);FatJet #eta;Events", 100, -7., 7.), "FatJet_0b_eta")
    histos["0b_msoftdrop"] = rdf.Histo1D((f"h_{sample_name}_FatJet_0b_msoftdrop", f"{label} (nBHad >=  0);Soft drop mass [GeV];Events", 100, 20., 120.), "FatJet_0b_msoftdrop")
    #On-Shell Tagger Scores
    histos["0b_ParT2_3b"] = rdf.Histo1D((f"h_{sample_name}_0b_ParT2_3b", f"{label} (nBHad >= 0);ParT2 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_0b_ParT2_3b_Normed")
    histos["0b_ParT2_4b"] = rdf.Histo1D((f"h_{sample_name}_0b_ParT2_4b", f"{label} (nBHad >= 0);ParT2 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_0b_ParT2_4b_Normed")
    histos["0b_ParT2_b_channels"] = rdf.Histo1D((f"h_{sample_name}_0b_ParT2_b_channels", f"{label} (nBHad >= 0);ParT2 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_0b_ParT2_b_channels_Normed")
    histos["0b_ParT3_3b"] = rdf.Histo1D((f"h_{sample_name}_0b_ParT3_3b", f"{label} (nBHad >= 0);ParT3 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_0b_ParT3_3b_Normed")
    histos["0b_ParT3_4b"] = rdf.Histo1D((f"h_{sample_name}_0b_ParT3_4b", f"{label} (nBHad >= 0);ParT3 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_0b_ParT3_4b_Normed")
    histos["0b_ParT3_b_channels"] = rdf.Histo1D((f"h_{sample_name}_0b_ParT3_b_channels", f"{label} (nBHad >= 0);ParT3 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_0b_ParT3_b_channels_Normed")
    
    #nBHad >= 1
    #Kinematics
    histos["1b_pt"] = rdf.Histo1D((f"h_{sample_name}_FatJet_1b_pt", f"{label} (nBHad >= 1);FatJet p_{{T}} [GeV];Events", 100, 100., 1000.), "FatJet_1b_pt")
    histos["1b_eta"] = rdf.Histo1D((f"h_{sample_name}_FatJet_1b_eta", f"{label} (nBHad >= 1);FatJet #eta;Events", 100, -7., 7.), "FatJet_1b_eta")
    histos["1b_msoftdrop"] = rdf.Histo1D((f"h_{sample_name}_FatJet_1b_msoftdrop", f"{label} (nBHad >=  0);Soft drop mass [GeV];Events", 100, 20., 120.), "FatJet_1b_msoftdrop")
    #On-Shell Tagger Scores
    histos["1b_ParT2_3b"] = rdf.Histo1D((f"h_{sample_name}_1b_ParT2_3b", f"{label} (nBHad >= 1);ParT2 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_1b_ParT2_3b_Normed")
    histos["1b_ParT2_4b"] = rdf.Histo1D((f"h_{sample_name}_1b_ParT2_4b", f"{label} (nBHad >= 1);ParT2 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_1b_ParT2_4b_Normed")
    histos["1b_ParT2_b_channels"] = rdf.Histo1D((f"h_{sample_name}_1b_ParT2_b_channels", f"{label} (nBHad >= 1);ParT2 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_1b_ParT2_b_channels_Normed")
    histos["1b_ParT3_3b"] = rdf.Histo1D((f"h_{sample_name}_1b_ParT3_3b", f"{label} (nBHad >= 1);ParT3 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_1b_ParT3_3b_Normed")
    histos["1b_ParT3_4b"] = rdf.Histo1D((f"h_{sample_name}_1b_ParT3_4b", f"{label} (nBHad >= 1);ParT3 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_1b_ParT3_4b_Normed")
    histos["1b_ParT3_b_channels"] = rdf.Histo1D((f"h_{sample_name}_1b_ParT3_b_channels", f"{label} (nBHad >= 1);ParT3 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_1b_ParT3_b_channels_Normed")

    #nBHad >= 2
    #Kinematics
    histos["2b_pt"] = rdf.Histo1D((f"h_{sample_name}_FatJet_2b_pt", f"{label} (nBHad >= 2);FatJet p_{{T}} [GeV];Events", 100, 100., 1000.), "FatJet_2b_pt")
    histos["2b_eta"] = rdf.Histo1D((f"h_{sample_name}_FatJet_2b_eta", f"{label} (nBHad >= 2);FatJet #eta;Events", 100, -7., 7.), "FatJet_2b_eta")
    histos["2b_msoftdrop"] = rdf.Histo1D((f"h_{sample_name}_FatJet_2b_msoftdrop", f"{label} (nBHad >=  0);Soft drop mass [GeV];Events", 100, 20., 120.), "FatJet_2b_msoftdrop")
    #On-Shell Tagger Scores
    histos["2b_ParT2_3b"] = rdf.Histo1D((f"h_{sample_name}_2b_ParT2_3b", f"{label} (nBHad >= 2);ParT2 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_2b_ParT2_3b_Normed")
    histos["2b_ParT2_4b"] = rdf.Histo1D((f"h_{sample_name}_2b_ParT2_4b", f"{label} (nBHad >= 2);ParT2 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_2b_ParT2_4b_Normed")
    histos["2b_ParT2_b_channels"] = rdf.Histo1D((f"h_{sample_name}_2b_ParT2_b_channels", f"{label} (nBHad >= 2);ParT2 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_2b_ParT2_b_channels_Normed")
    histos["2b_ParT3_3b"] = rdf.Histo1D((f"h_{sample_name}_2b_ParT3_3b", f"{label} (nBHad >= 2);ParT3 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_2b_ParT3_3b_Normed")
    histos["2b_ParT3_4b"] = rdf.Histo1D((f"h_{sample_name}_2b_ParT3_4b", f"{label} (nBHad >= 2);ParT3 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_2b_ParT3_4b_Normed")
    histos["2b_ParT3_b_channels"] = rdf.Histo1D((f"h_{sample_name}_2b_ParT3_b_channels", f"{label} (nBHad >= 2);ParT3 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_2b_ParT3_b_channels_Normed")

    #nBHad >= 3
    #Kinematics
    histos["3b_pt"] = rdf.Histo1D((f"h_{sample_name}_FatJet_3b_pt", f"{label} (nBHad >= 3);FatJet p_{{T}} [GeV];Events", 100, 100., 1000.), "FatJet_3b_pt")
    histos["3b_eta"] = rdf.Histo1D((f"h_{sample_name}_FatJet_3b_eta", f"{label} (nBHad >= 3);FatJet #eta;Events", 100, -7., 7.), "FatJet_3b_eta")
    histos["3b_msoftdrop"] = rdf.Histo1D((f"h_{sample_name}_FatJet_3b_msoftdrop", f"{label} (nBHad >=  0);Soft drop mass [GeV];Events", 100, 20., 120.), "FatJet_3b_msoftdrop")
    #On-Shell Tagger Scores
    histos["3b_ParT2_3b"] = rdf.Histo1D((f"h_{sample_name}_3b_ParT2_3b", f"{label} (nBHad >= 3);ParT2 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_3b_ParT2_3b_Normed")
    histos["3b_ParT2_4b"] = rdf.Histo1D((f"h_{sample_name}_3b_ParT2_4b", f"{label} (nBHad >= 3);ParT2 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_3b_ParT2_4b_Normed")
    histos["3b_ParT2_b_channels"] = rdf.Histo1D((f"h_{sample_name}_3b_ParT2_b_channels", f"{label} (nBHad >= 3);ParT2 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_3b_ParT2_b_channels_Normed")
    histos["3b_ParT3_3b"] = rdf.Histo1D((f"h_{sample_name}_3b_ParT3_3b", f"{label} (nBHad >= 3);ParT3 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_3b_ParT3_3b_Normed")
    histos["3b_ParT3_4b"] = rdf.Histo1D((f"h_{sample_name}_3b_ParT3_4b", f"{label} (nBHad >= 3);ParT3 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_3b_ParT3_4b_Normed")
    histos["3b_ParT3_b_channels"] = rdf.Histo1D((f"h_{sample_name}_3b_ParT3_b_channels", f"{label} (nBHad >= 3);ParT3 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_3b_ParT3_b_channels_Normed")

    #nBHad >= 4
    #Kinematics
    histos["4b_pt"] = rdf.Histo1D((f"h_{sample_name}_FatJet_4b_pt", f"{label} (nBHad >= 4);FatJet p_{{T}} [GeV];Events", 100, 100., 1000.), "FatJet_4b_pt")
    histos["4b_eta"] = rdf.Histo1D((f"h_{sample_name}_FatJet_4b_eta", f"{label} (nBHad >= 4);FatJet #eta;Events", 100, -7., 7.), "FatJet_4b_eta")
    histos["4b_msoftdrop"] = rdf.Histo1D((f"h_{sample_name}_FatJet_4b_msoftdrop", f"{label} (nBHad >=  0);Soft drop mass [GeV];Events", 100, 20., 120.), "FatJet_4b_msoftdrop")
    #On-Shell Tagger Scores
    histos["4b_ParT2_3b"] = rdf.Histo1D((f"h_{sample_name}_4b_ParT2_3b", f"{label} (nBHad >= 4);ParT2 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_4b_ParT2_3b_Normed")
    histos["4b_ParT2_4b"] = rdf.Histo1D((f"h_{sample_name}_4b_ParT2_4b", f"{label} (nBHad >= 4);ParT2 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_4b_ParT2_4b_Normed")
    histos["4b_ParT2_b_channels"] = rdf.Histo1D((f"h_{sample_name}_4b_ParT2_b_channels", f"{label} (nBHad >= 4);ParT2 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_4b_ParT2_b_channels_Normed")
    histos["4b_ParT3_3b"] = rdf.Histo1D((f"h_{sample_name}_4b_ParT3_3b", f"{label} (nBHad >= 4);ParT3 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_4b_ParT3_3b_Normed")
    histos["4b_ParT3_4b"] = rdf.Histo1D((f"h_{sample_name}_4b_ParT3_4b", f"{label} (nBHad >= 4);ParT3 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_4b_ParT3_4b_Normed")
    histos["4b_ParT3_b_channels"] = rdf.Histo1D((f"h_{sample_name}_4b_ParT3_b_channels", f"{label} (nBHad >= 4);ParT3 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_4b_ParT3_b_channels_Normed")

    return histos

#Now, let's make a function to save our histograms in .ROOT files. We'll make one file per dataset/sample.

def save_histograms(histos, output_dir="histograms"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for sample_name, sample_histos in histos.items():
        output_filename = output_dir / f"FatJet_Histograms_{sample_name}.root"

        outfile = ROOT.TFile(str(output_filename), "RECREATE")

        if not outfile or outfile.IsZombie():
            raise RuntimeError(f"Could not create output file: {output_filename}")

        outfile.cd()

        for hist_name, hist_proxy in sample_histos.items():
            # Force the RDataFrame event loop.
            hist = hist_proxy.GetValue()

            # Save histogram directly in this sample's ROOT file.
            hist.Write(hist_name)

            print(f"Wrote {hist_name} to {output_filename}")

        outfile.Close()
        print(f"Saved {output_filename}")


"""
#Additional Histograms including Off-Shell Z and Z*. ParT2 Type 1 and Type 2.
h_FatJet_4b_ParT2_3b_1 = rdf.Histo1D(("FatJet_4b_ParT2_3b_1", "FatJet HtoAAto4b Tagger Score (ZZ*); ParT2 bbb v QCD; Events", 100, 0., 1.), "FatJet_4b_ParT2_3b_adv1")
h_FatJet_4b_ParT2_4b_1 = rdf.Histo1D(("FatJet_4b_ParT2_4b_1", "FatJet HtoAAto4b Tagger Score (ZZ*); ParT2 bbbb v QCD; Events", 100, 0., 1.), "FatJet_4b_ParT2_4b_adv1")
h_FatJet_4b_ParT2_3b_2 = rdf.Histo1D(("FatJet_4b_ParT2_3b_2", "FatJet HtoAAto4b Tagger Score (ZZ); ParT2 bbb v QCD; Events", 100, 0., 1.), "FatJet_4b_ParT2_3b_adv2")
h_FatJet_4b_ParT2_4b_2 = rdf.Histo1D(("FatJet_4b_ParT2_4b_2", "FatJet HtoAAto4b Tagger Score (ZZ); ParT2 bbbb v QCD; Events", 100, 0., 1.), "FatJet_4b_ParT2_4b_adv2")

#Additional Histograms including Off-Shell Z and Z*. ParT3 Type 1 and Type 2.
h_FatJet_4b_ParT3_3b_1 = rdf.Histo1D(("FatJet_4b_ParT3_3b_1", "FatJet HtoAAto4b Tagger Score (ZZ*); ParT3 bbb v QCD; Events", 100, 0., 1.), "FatJet_4b_ParT3_3b_adv1")
h_FatJet_4b_ParT3_4b_1 = rdf.Histo1D(("FatJet_4b_ParT3_4b_1", "FatJet HtoAAto4b Tagger Score (ZZ*); ParT3 bbbb v QCD; Events", 100, 0., 1.), "FatJet_4b_ParT3_4b_adv1")
h_FatJet_4b_ParT3_3b_2 = rdf.Histo1D(("FatJet_4b_ParT3_3b_2", "FatJet HtoAAto4b Tagger Score (ZZ); ParT3 bbb v QCD; Events", 100, 0., 1.), "FatJet_4b_ParT3_3b_adv2")
h_FatJet_4b_ParT3_4b_2 = rdf.Histo1D(("FatJet_4b_ParT3_4b_2", "FatJet HtoAAto4b Tagger Score (ZZ); ParT3 bbbb v QCD; Events", 100, 0., 1.), "FatJet_4b_ParT3_4b_adv2")
"""


#Now we'll generate our histograms. 
histos = {}

for sample_name, rdf in rdf_defined.items():
    histos[sample_name] = book_histograms(rdf, sample_name, samples[sample_name]["label"])

#Finally, we'll save them.
save_histograms(histos, output_dir="nBH_cut_histograms")



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Example 1: Select only GenParticles with status 1 and pt > 10 GeV
# GenPart_pt is typically a ROOT::RVec<float>
# rdf_gen = rdf.Filter("GenPart_status == 1 && GenPart_pt > 10.0")

# Example 2: Define a new column (e.g., Rapidity) using a lambda function
# The function acts on the whole RVec for each event
#rdf_with_rapidity = rdf_gen.Define("GenPart_rapidity",
#                                 "0.5 * log((sqrt(GenPart_mass*GenPart_mass + GenPart_pt*GenPart_pt*cosh(GenPart_eta)*cosh(GenPart_eta)) + GenPart_pt*sinh(GenPart_eta)) / (sqrt(GenPart_mass*GenPart_mass + GenPart_pt*GenPart_pt*cosh(GenPart_eta)*cosh(GenPart_eta)) - GenPart_pt*sinh(GenPart_eta)))")

# Example 3: Histogramming PT of specific GenParticles
#hist_gen_pt = rdf_with_rapidity.Histo1D(("gen_pt", "GenPart Pt;Pt [GeV];Counts", 100, 0, 100), "GenPart_pt")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
"""
# Save the histogram
outfile = ROOT.TFile("Higgs_Gen_HISTOS_RAW.root", "RECREATE")

#Save Gen-Level kinematic histograms
#Gen-Level First
h_Higgs_GenFirst_pt.Write()
h_Higgs_GenFirst_phi.Write()
h_Higgs_GenFirst_eta.Write()
h_Higgs_GenFirst_mass.Write()
#Gen-Level Last
h_Higgs_GenLast_pt.Write()
h_Higgs_GenLast_phi.Write()
h_Higgs_GenLast_eta.Write()
h_Higgs_GenLast_mass.Write()
#Gen-Level 2D
h2_HiggsPt_GenFirst_GenLast.Write()

outfile.Close()
"""

