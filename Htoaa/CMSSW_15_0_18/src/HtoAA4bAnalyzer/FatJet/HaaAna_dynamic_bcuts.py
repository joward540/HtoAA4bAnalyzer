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

    "QCD0B1": {
        "subdir": "QCD0B-4Jets_Bin-HT-40to70_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-40to70_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 40-70",
    },

    "QCD0B2": {
        "subdir": "QCD0B-4Jets_Bin-HT-70to100_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-70to100_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 70-100",
    },

    "QCD0B3": {
        "subdir": "QCD0B-4Jets_Bin-HT-100to200_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-100to200_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 100-200",
    },

    "QCD0B4": {
        "subdir": "QCD0B-4Jets_Bin-HT-200to400_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-200to400_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 200-400",
    },

    "QCD0B5": {
        "subdir": "QCD0B-4Jets_Bin-HT-400to600_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-400to600_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 400-600",
    },

    "QCD0B6": {
        "subdir": "QCD0B-4Jets_Bin-HT-600to800_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-600to800_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 600-800",
    },

    "QCD0B7": {
        "subdir": "QCD0B-4Jets_Bin-HT-800to1000_Fil-BPS_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-800to1000_Fil-BPS_13p6TeV_job*.root",
        "label": "QCD0B HT 800-1000",
    },

    "QCD0B8": {
        "subdir": "QCD0B-4Jets_Bin-HT-1000to1200_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-1000to1200_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 1000-1200",
    },

    "QCD0B9": {
        "subdir": "QCD0B-4Jets_Bin-HT-1200to1500_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-1200to1500_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 1200-1500",
    },

    "QCD0B10": {
        "subdir": "QCD0B-4Jets_Bin-HT-1500to2000_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-1500to2000_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 1500-2000",
    },

    "QCD0B11": {
        "subdir": "QCD0B-4Jets_Bin-HT-2000_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-2000_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 2000",
    },

    "QCDB1": {
        "subdir": "QCD0B-4Jets_Bin-HT-40to100_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCD0B-4Jets_Bin-HT-40to100_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCD0B HT 40-100",
    },

    "QCDB2": {
        "subdir": "QCDB-4Jets_Bin-HT-100to200_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCDB-4Jets_Bin-HT-100to200_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCDB HT 100-200",
    },

    "QCDB3": {
        "subdir": "QCDB-4Jets_Bin-HT-200to400_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCDB-4Jets_Bin-HT-200to400_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCDB HT 200-400",
    },

    "QCDB4": {
        "subdir": "QCDB-4Jets_Bin-HT-400to600_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCDB-4Jets_Bin-HT-400to600_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCDB HT 400-600",
    },

    "QCDB5": {
        "subdir": "QCDB-4Jets_Bin-HT-800to1000_Fil-BPS_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCDB-4Jets_Bin-HT-800to1000_Fil-BPS_13p6TeV_job*.root",
        "label": "QCDB HT 800-1000",
    },

    "QCDB6": {
        "subdir": "QCDB-4Jets_Bin-HT-1000to1500_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCDB-4Jets_Bin-HT-1000to1500_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCDB HT 1000-1500",
    },

    "QCDB7": {
        "subdir": "QCDB-4Jets_Bin-HT-1500to2000_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCDB-4Jets_Bin-HT-1500to2000_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCDB HT 1500-2000",
    },

    "QCDB8": {
        "subdir": "QCDB-4Jets_Bin-HT-2000_Fil-BPS_TuneCP5_13p6TeV",
        "pattern": "Summer24NanoAODv15_QCDB-4Jets_Bin-HT-2000_Fil-BPS_TuneCP5_13p6TeV_job*.root",
        "label": "QCDB HT 2000",
    },

}

#This will allow us to make an argument after calling the script. If we don't include an argument, we'll run for all datasets. If we do include it, we'll only run for one dataset.
parser = argparse.ArgumentParser(description="Make FatJet histograms for HtoAA samples.")

parser.add_argument(
    "dataset",
    nargs="?",
    choices=list(samples.keys()),
    help="Optional dataset to run. If omitted, all datasets run.",
)
parser.add_argument(
    "--max-files",
    type=int,
    default=None,
    help="Maximum number of ROOT files to use per dataset for testing.",
)
parser.add_argument(
    "--b-cuts",
    nargs="+",
    type=int,
    default=[0, 1, 2, 3, 4],
    metavar="N",
    help=(
        "Minimum GenJetAK8_nBHadrons thresholds to build. "
        "Examples: '--b-cuts 4' or '--b-cuts 0 2 4'. "
        "Default: 0 1 2 3 4."
    ),
)
parser.add_argument(
    "--cumulative",
    choices=("none", "scores", "all"),
    default="scores",
    help=(
        "Choose which ordinary histograms also receive cumulative copies. "
        "'scores' makes cumulative ParT2/ParT3 score histograms, 'all' also "
        "includes kinematics, and 'none' disables cumulative output. "
        "Default: scores."
    ),
)
parser.add_argument(
    "--cumulative-direction",
    choices=("above", "below"),
    default="above",
    help=(
        "Cumulative direction. 'above' stores entries at or above each bin's "
        "lower edge; 'below' stores entries at or below each bin's upper edge. "
        "Default: above."
    ),
)
parser.add_argument(
    "--normalize-cumulative",
    action="store_true",
    help="Normalize cumulative histograms to fractions between 0 and 1.",
)


args = parser.parse_args()

invalid_b_cuts = [cut for cut in args.b_cuts if cut < 0 or cut > 4]
if invalid_b_cuts:
    parser.error(
        "--b-cuts values must be integers from 0 through 4; "
        f"received: {invalid_b_cuts}"
    )

# Remove duplicates and use a deterministic order.
b_cuts = sorted(set(args.b_cuts))
print(f"Building nBHad selections for thresholds: {b_cuts}")
print("Cumulative histograms: "\n, f"mode={args.cumulative}, direction={args.cumulative_direction}, "\n, f"normalized={args.normalize_cumulative}")

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


# One helper handles every nBHad threshold. The third argument is the selected
# minimum number of b hadrons: 0, 1, 2, 3, or 4.
ROOT.gInterpreter.Declare("""
#include "ROOT/RVec.hxx"
#include <cstddef>

ROOT::RVec<std::size_t> getFatJetIdx(
    const ROOT::RVecI& FatJet_genJetAK8Idx,
    const ROOT::RVecI& GenJetAK8_nBHadrons,
    int minBHadrons
) {
    ROOT::RVec<std::size_t> idxs;

    for (std::size_t i = 0; i < FatJet_genJetAK8Idx.size(); ++i) {
        const int genIdx = FatJet_genJetAK8Idx[i];

        if (genIdx >= 0 &&
            static_cast<std::size_t>(genIdx) < GenJetAK8_nBHadrons.size() &&
            GenJetAK8_nBHadrons[genIdx] >= minBHadrons) {
            idxs.push_back(i);
        }
    }

    return idxs;
}
""")

#We'll define a pt_min so that we can cut there as well.
pt_min = 150.

#Let's set up a mask to make sure we only investigate events with some tagger score in the desired final state. "FatJet_pt > 300" getHas4bScoreMask(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons)")
def define_ParT_variables(rdf, selected_b_cuts):
    

    # First we'll calculate variables with no nBHad or pT cuts applied.
    
    #Kinematic variables for full datasets.
    rdf = rdf.Define("FatJet_pt_full", "FatJet_pt")\
             .Define("FatJet_eta_full", "FatJet_eta")\
             .Define("FatJet_msoftdrop_full", "FatJet_msoftdrop")
    
    #Particle Transformer V2 Variables (Full dataset).
    #On-shell ParT2
    rdf = rdf.Define("FatJet_ParT2_3b_full", "FatJet_globalParT2_probHZxZxbbb")\
             .Define("FatJet_ParT2_4b_full", "FatJet_globalParT2_probHZxZxbbbb")\
             .Define("FatJet_ParT2_b_channels_full", "FatJet_ParT2_3b_full + FatJet_ParT2_4b_full")\
             .Define("FatJet_ParT2_QCD_full", "FatJet_globalParT2_probQCDb + FatJet_globalParT2_probQCDbb + FatJet_globalParT2_probQCDc + FatJet_globalParT2_probQCDcc + FatJet_globalParT2_probQCDothers")\
             .Define("FatJet_ParT2_3b_full_Normed", "FatJet_ParT2_3b_full / (FatJet_ParT2_3b_full + FatJet_ParT2_QCD_full)")\
             .Define("FatJet_ParT2_4b_full_Normed", "FatJet_ParT2_4b_full / (FatJet_ParT2_4b_full + FatJet_ParT2_QCD_full)")\
             .Define("FatJet_ParT2_b_channels_full_Normed", "FatJet_ParT2_b_channels_full / (FatJet_ParT2_b_channels_full + FatJet_ParT2_QCD_full)")
    #Off-shell ParT2
    rdf = rdf.Define("FatJet_ParT2_3b_adv1_full", "FatJet_globalParT2_probHZxZxStarbbb")\
             .Define("FatJet_ParT2_4b_adv1_full", "FatJet_globalParT2_probHZxZxStarbbbb")\
             .Define("FatJet_ParT2_b_channels_adv1_full","FatJet_ParT2_3b_adv1_full + FatJet_ParT2_4b_adv1_full")\
             .Define("FatJet_ParT2_3b_adv1_full_Normed", "FatJet_ParT2_3b_adv1_full / (FatJet_ParT2_3b_adv1_full +  FatJet_ParT2_QCD_full)")\
             .Define("FatJet_ParT2_4b_adv1_full_Normed", "FatJet_ParT2_4b_adv1_full /(FatJet_ParT2_4b_adv1_full +  FatJet_ParT2_QCD_full)")\
             .Define("FatJet_ParT2_b_channels_adv1_full_Normed","FatJet_ParT2_b_channels_adv1_full / (FatJet_ParT2_b_channels_adv1_full + FatJet_ParT2_QCD_full)")\
             .Define("FatJet_ParT2_3b_adv2_full", "FatJet_globalParT2_probHZZbbb")\
             .Define("FatJet_ParT2_4b_adv2_full", "FatJet_globalParT2_probHZZbbbb")\
             .Define("FatJet_ParT2_b_channels_adv2_full","FatJet_ParT2_3b_adv2_full + FatJet_ParT2_4b_adv2_full")\
             .Define("FatJet_ParT2_3b_adv2_full_Normed", "FatJet_ParT2_3b_adv2_full / (FatJet_ParT2_3b_adv2_full +  FatJet_ParT2_QCD_full)")\
             .Define("FatJet_ParT2_4b_adv2_full_Normed", "FatJet_ParT2_4b_adv2_full / (FatJet_ParT2_4b_adv2_full +  FatJet_ParT2_QCD_full)")\
             .Define("FatJet_ParT2_b_channels_adv2_full_Normed","FatJet_ParT2_b_channels_adv2_full / (FatJet_ParT2_b_channels_adv2_full + FatJet_ParT2_QCD_full)")

    #Particle Transformer V3 variables (Full Dataset).
    #On-shell ParT3
    rdf = rdf.Define("FatJet_ParT3_3b_full", "FatJet_globalParT3_probRawHZxZxbbb")\
             .Define("FatJet_ParT3_4b_full", "FatJet_globalParT3_probRawHZxZxbbbb")\
             .Define("FatJet_ParT3_b_channels_full", "FatJet_ParT3_3b_full + FatJet_ParT3_4b_full")\
             .Define("FatJet_ParT3_QCD_full", "FatJet_globalParT3_QCD")\
             .Define("FatJet_ParT3_3b_full_Normed", "FatJet_ParT3_3b_full / (FatJet_ParT3_3b_full + FatJet_ParT3_QCD_full)")\
             .Define("FatJet_ParT3_4b_full_Normed", "FatJet_ParT3_4b_full / (FatJet_ParT3_4b_full + FatJet_ParT3_QCD_full)")\
             .Define("FatJet_ParT3_b_channels_full_Normed", "FatJet_ParT3_b_channels_full / (FatJet_ParT3_b_channels_full + FatJet_ParT3_QCD_full)")
    #Of-shell ParT3
    rdf = rdf.Define("FatJet_ParT3_3b_adv1_full", "FatJet_globalParT3_probRawHZxZxStarbbb")\
             .Define("FatJet_ParT3_4b_adv1_full", "FatJet_globalParT3_probRawHZxZxStarbbbb")\
             .Define("FatJet_ParT3_b_channels_adv1_full","FatJet_ParT3_3b_adv1_full + FatJet_ParT3_4b_adv1_full")\
             .Define("FatJet_ParT3_3b_adv1_full_Normed", "FatJet_ParT3_3b_adv1_full / (FatJet_ParT3_3b_adv1_full +  FatJet_ParT3_QCD_full)")\
             .Define("FatJet_ParT3_4b_adv1_full_Normed", "FatJet_ParT3_4b_adv1_full /(FatJet_ParT3_4b_adv1_full +  FatJet_ParT3_QCD_full)")\
             .Define("FatJet_ParT3_b_channels_adv1_full_Normed","FatJet_ParT3_b_channels_adv1_full / (FatJet_ParT3_b_channels_adv1_full + FatJet_ParT3_QCD_full)")\
             .Define("FatJet_ParT3_3b_adv2_full", "FatJet_globalParT3_probRawHZZbbb")\
             .Define("FatJet_ParT3_4b_adv2_full", "FatJet_globalParT3_probRawHZZbbbb")\
             .Define("FatJet_ParT3_b_channels_adv2_full","FatJet_ParT3_3b_adv2_full + FatJet_ParT3_4b_adv2_full")\
             .Define("FatJet_ParT3_3b_adv2_full_Normed", "FatJet_ParT3_3b_adv2_full / (FatJet_ParT3_3b_adv2_full +  FatJet_ParT3_QCD_full)")\
             .Define("FatJet_ParT3_4b_adv2_full_Normed", "FatJet_ParT3_4b_adv2_full / (FatJet_ParT3_4b_adv2_full +  FatJet_ParT3_QCD_full)")\
             .Define("FatJet_ParT3_b_channels_adv2_full_Normed","FatJet_ParT3_b_channels_adv2_full / (FatJet_ParT3_b_channels_adv2_full + FatJet_ParT3_QCD_full)")

    # Build the same set of columns for each requested nBHad threshold.
    for b_cut in selected_b_cuts:
        prefix = f"FatJet_{b_cut}b"
        idx_col = f"{prefix}_idx"
        trimmed_idx_col = f"{prefix}_trimmed_idx"

        rdf = rdf.Define(idx_col, f"getFatJetIdx(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons, {b_cut})")
        rdf = rdf.Define(trimmed_idx_col, f"{idx_col}[Take(FatJet_pt, {idx_col}) > {pt_min}]")

        #Variables with nBHadrons selection cut applied
        #Kinematics (nBH cut)
        rdf = rdf.Define(f"{prefix}_pt", f"Take(FatJet_pt, {trimmed_idx_col})")\
                 .Define(f"{prefix}_eta", f"Take(FatJet_eta, {trimmed_idx_col})")\
                 .Define(f"{prefix}_msoftdrop", f"Take(FatJet_msoftdrop, {trimmed_idx_col})")
        
        #Particle Transformer V2 variables (nBH cut)
        #On-shell ParT2
        rdf = rdf.Define(f"{prefix}_ParT2_3b", f"Take(FatJet_globalParT2_probHZxZxbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT2_4b", f"Take(FatJet_globalParT2_probHZxZxbbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT2_b_channels", f"{prefix}_ParT2_3b + {prefix}_ParT2_4b")\
                 .Define(f"{prefix}_ParT2_QCD", f"Take(FatJet_globalParT2_probQCDb, {trimmed_idx_col}) + Take(FatJet_globalParT2_probQCDbb, {trimmed_idx_col}) + Take(FatJet_globalParT2_probQCDc, {trimmed_idx_col}) + Take(FatJet_globalParT2_probQCDcc, {trimmed_idx_col}) + Take(FatJet_globalParT2_probQCDothers, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT2_3b_Normed", f"{prefix}_ParT2_3b / ({prefix}_ParT2_3b + {prefix}_ParT2_QCD)")\
                 .Define(f"{prefix}_ParT2_4b_Normed", f"{prefix}_ParT2_4b / ({prefix}_ParT2_4b + {prefix}_ParT2_QCD)")\
                 .Define(f"{prefix}_ParT2_b_channels_Normed", f"{prefix}_ParT2_b_channels / ({prefix}_ParT2_b_channels + {prefix}_ParT2_QCD)")        
        #Off-shel ParT2
        rdf = rdf.Define(f"{prefix}_ParT2_3b_adv1", f"Take(FatJet_globalParT2_probHZxZxStarbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT2_4b_adv1", f"Take(FatJet_globalParT2_probHZxZxStarbbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT2_b_channels_adv1", f"{prefix}_ParT2_3b_adv1 + {prefix}_ParT2_4b_adv1")\
                 .Define(f"{prefix}_ParT2_3b_adv1_Normed", f"{prefix}_ParT2_3b_adv1 / ({prefix}_ParT2_3b_adv1 + {prefix}_ParT2_QCD)")\
                 .Define(f"{prefix}_ParT2_4b_adv1_Normed", f"{prefix}_ParT2_4b_adv1 / ({prefix}_ParT2_4b_adv1 + {prefix}_ParT2_QCD)")\
                 .Define(f"{prefix}_ParT2_b_channels_adv1_Normed", f"{prefix}_ParT2_b_channels_adv1 / ({prefix}_ParT2_b_channels_adv1 + {prefix}_ParT2_QCD)")\
                 .Define(f"{prefix}_ParT2_3b_adv2", f"Take(FatJet_globalParT2_probHZZbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT2_4b_adv2", f"Take(FatJet_globalParT2_probHZZbbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT2_b_channels_adv2", f"{prefix}_ParT2_3b_adv2 + {prefix}_ParT2_4b_adv2")\
                 .Define(f"{prefix}_ParT2_3b_adv2_Normed", f"{prefix}_ParT2_3b_adv2 / ({prefix}_ParT2_3b_adv2 + {prefix}_ParT2_QCD)")\
                 .Define(f"{prefix}_ParT2_4b_adv2_Normed", f"{prefix}_ParT2_4b_adv2 / ({prefix}_ParT2_4b_adv2 + {prefix}_ParT2_QCD)")\
                 .Define(f"{prefix}_ParT2_b_channels_adv2_Normed", f"{prefix}_ParT2_b_channels_adv2 / ({prefix}_ParT2_b_channels_adv2 + {prefix}_ParT2_QCD)")
        
       #Particle Transformer V3 variables (nBH cut)
       #On-shell ParT3
        rdf = rdf.Define(f"{prefix}_ParT3_3b", f"Take(FatJet_globalParT3_probRawHZxZxbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT3_4b", f"Take(FatJet_globalParT3_probRawHZxZxbbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT3_b_channels", f"{prefix}_ParT3_3b + {prefix}_ParT3_4b")\
                 .Define(f"{prefix}_ParT3_QCD", f"Take(FatJet_globalParT3_QCD, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT3_3b_Normed", f"{prefix}_ParT3_3b / ({prefix}_ParT3_3b + {prefix}_ParT3_QCD)")\
                 .Define(f"{prefix}_ParT3_4b_Normed", f"{prefix}_ParT3_4b / ({prefix}_ParT3_4b + {prefix}_ParT3_QCD)")\
                 .Define(f"{prefix}_ParT3_b_channels_Normed", f"{prefix}_ParT3_b_channels / ({prefix}_ParT3_b_channels + {prefix}_ParT3_QCD)")
        #Off-shell ParT3
        rdf = rdf.Define(f"{prefix}_ParT3_3b_adv1", f"Take(FatJet_globalParT3_probRawHZxZxStarbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT3_4b_adv1", f"Take(FatJet_globalParT3_probRawHZxZxStarbbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT3_b_channels_adv1", f"{prefix}_ParT3_3b_adv1 + {prefix}_ParT3_4b_adv1")\
                 .Define(f"{prefix}_ParT3_3b_adv1_Normed", f"{prefix}_ParT3_3b_adv1 / ({prefix}_ParT3_3b_adv1 + {prefix}_ParT3_QCD)")\
                 .Define(f"{prefix}_ParT3_4b_adv1_Normed", f"{prefix}_ParT3_4b_adv1 / ({prefix}_ParT3_4b_adv1 + {prefix}_ParT3_QCD)")\
                 .Define(f"{prefix}_ParT3_b_channels_adv1_Normed", f"{prefix}_ParT3_b_channels_adv1 / ({prefix}_ParT3_b_channels_adv1 + {prefix}_ParT3_QCD)")\
                 .Define(f"{prefix}_ParT3_3b_adv2", f"Take(FatJet_globalParT3_probRawHZZbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT3_4b_adv2", f"Take(FatJet_globalParT3_probRawHZZbbbb, {trimmed_idx_col})")\
                 .Define(f"{prefix}_ParT3_b_channels_adv2", f"{prefix}_ParT3_3b_adv2 + {prefix}_ParT3_4b_adv2")\
                 .Define(f"{prefix}_ParT3_3b_adv2_Normed", f"{prefix}_ParT3_3b_adv2 / ({prefix}_ParT3_3b_adv2 + {prefix}_ParT3_QCD)")\
                 .Define(f"{prefix}_ParT3_4b_adv2_Normed", f"{prefix}_ParT3_4b_adv2 / ({prefix}_ParT3_4b_adv2 + {prefix}_ParT3_QCD)")\
                 .Define(f"{prefix}_ParT3_b_channels_adv2_Normed", f"{prefix}_ParT3_b_channels_adv2 / ({prefix}_ParT3_b_channels_adv2 + {prefix}_ParT3_QCD)")


    return rdf


#Now we're ready to generate multiple RDataFrames
rdf_defined = {}

for sample_name, rdf in sample_rdf.items():
    rdf_defined[sample_name] = define_ParT_variables(rdf, b_cuts)


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

def book_histograms(rdf, sample_name, label, selected_b_cuts):
    """Book full histograms and histograms for the requested nBHad cuts."""
    histos = {}

    # Full, uncut histograms.
    histos["pt"] = rdf.Histo1D((f"h_{sample_name}_FatJet_pt", f"{label};FatJet p_{{T}} [GeV];Events", 100, 100.0, 1000.0), "FatJet_pt_full")
    histos["eta"] = rdf.Histo1D((f"h_{sample_name}_FatJet_eta", f"{label};FatJet #eta;Events", 100, -7.0, 7.0), "FatJet_eta_full")
    histos["msoftdrop"] = rdf.Histo1D((f"h_{sample_name}_FatJet_msoftdrop", f"{label};Soft drop mass [GeV];Events", 100, 20.0, 120.0), "FatJet_msoftdrop_full")
    histos["ParT2_3b"] = rdf.Histo1D((f"h_{sample_name}_ParT2_3b", f"{label};ParT2 bbb / (bbb + QCD);Events", 100, 0.0, 1.0), "FatJet_ParT2_3b_full_Normed")
    histos["ParT2_4b"] = rdf.Histo1D((f"h_{sample_name}_ParT2_4b", f"{label};ParT2 bbbb / (bbbb + QCD);Events", 100, 0.0, 1.0), "FatJet_ParT2_4b_full_Normed")
    histos["ParT2_b_channels"] = rdf.Histo1D((f"h_{sample_name}_ParT2_b_channels", f"{label};ParT2 3b + 4b / (3b + 4b + QCD);Events", 100, 0.0, 1.0), "FatJet_ParT2_b_channels_full_Normed")
    histos["ParT3_3b"] = rdf.Histo1D((f"h_{sample_name}_ParT3_3b", f"{label};ParT3 bbb / (bbb + QCD);Events", 100, 0.0, 1.0), "FatJet_ParT3_3b_full_Normed")
    histos["ParT3_4b"] = rdf.Histo1D((f"h_{sample_name}_ParT3_4b", f"{label};ParT3 bbbb / (bbbb + QCD);Events", 100, 0.0, 1.0), "FatJet_ParT3_4b_full_Normed")
    histos["ParT3_b_channels"] = rdf.Histo1D((f"h_{sample_name}_ParT3_b_channels", f"{label};ParT3 3b + 4b / (3b + 4b + QCD);Events", 100, 0.0, 1.0), "FatJet_ParT3_b_channels_full_Normed")

    # Book the same histogram set for every requested threshold.
    for b_cut in selected_b_cuts:
        key_prefix = f"{b_cut}b"
        column_prefix = f"FatJet_{key_prefix}"
        cut_label = f"{label} (nBHad >= {b_cut})"

        histos[f"{key_prefix}_pt"] = rdf.Histo1D((f"h_{sample_name}_FatJet_{key_prefix}_pt", f"{cut_label};FatJet p_{{T}} [GeV];Events", 100, 100.0, 1000.0), f"{column_prefix}_pt")
        histos[f"{key_prefix}_eta"] = rdf.Histo1D((f"h_{sample_name}_FatJet_{key_prefix}_eta", f"{cut_label};FatJet #eta;Events", 100, -7.0, 7.0), f"{column_prefix}_eta")
        histos[f"{key_prefix}_msoftdrop"] = rdf.Histo1D((f"h_{sample_name}_FatJet_{key_prefix}_msoftdrop", f"{cut_label};Soft drop mass [GeV];Events", 100, 20.0, 120.0), f"{column_prefix}_msoftdrop")
        histos[f"{key_prefix}_ParT2_3b"] = rdf.Histo1D((f"h_{sample_name}_{key_prefix}_ParT2_3b", f"{cut_label};ParT2 bbb / (bbb + QCD);Events", 100, 0.0, 1.0), f"{column_prefix}_ParT2_3b_Normed")
        histos[f"{key_prefix}_ParT2_4b"] = rdf.Histo1D((f"h_{sample_name}_{key_prefix}_ParT2_4b", f"{cut_label};ParT2 bbbb / (bbbb + QCD);Events", 100, 0.0, 1.0), f"{column_prefix}_ParT2_4b_Normed")
        histos[f"{key_prefix}_ParT2_b_channels"] = rdf.Histo1D((f"h_{sample_name}_{key_prefix}_ParT2_b_channels", f"{cut_label};ParT2 3b + 4b / (3b + 4b + QCD);Events", 100, 0.0, 1.0), f"{column_prefix}_ParT2_b_channels_Normed")
        histos[f"{key_prefix}_ParT3_3b"] = rdf.Histo1D((f"h_{sample_name}_{key_prefix}_ParT3_3b", f"{cut_label};ParT3 bbb / (bbb + QCD);Events", 100, 0.0, 1.0), f"{column_prefix}_ParT3_3b_Normed")
        histos[f"{key_prefix}_ParT3_4b"] = rdf.Histo1D((f"h_{sample_name}_{key_prefix}_ParT3_4b", f"{cut_label};ParT3 bbbb / (bbbb + QCD);Events", 100, 0.0, 1.0), f"{column_prefix}_ParT3_4b_Normed")
        histos[f"{key_prefix}_ParT3_b_channels"] = rdf.Histo1D((f"h_{sample_name}_{key_prefix}_ParT3_b_channels", f"{cut_label};ParT3 3b + 4b / (3b + 4b + QCD);Events", 100, 0.0, 1.0), f"{column_prefix}_ParT3_b_channels_Normed")

    return histos

#Save histogram suffixes.
SCORE_HISTOGRAM_SUFFIXES = (
    "ParT2_3b",
    "ParT2_4b",
    "ParT2_b_channels",
    "ParT3_3b",
    "ParT3_4b",
    "ParT3_b_channels",
)

#Let's make a flag for the cumulative histograms.
def cumulative_flag(hist_name, cumulative_mode):

    if cumulative_mode == "none":
        return False

    if cumulative_mode == "all":
        return True


    return any(hist_name == suffix or hist_name.endswith(f"_{suffix}") for suffix in SCORE_HISTOGRAM_SUFFIXES)


#Here's our function for generating cumultative histograms.
def make_cumulative_histogram(hist, direction="above", normalize=False):
    if direction not in {"above", "below"}:
        raise ValueError("Direction must be 'above' or 'below'")

    cumulative = hist.Clone(f"{hist.GetName()}_cumulative")
    cumulative.SetDirectory(0)

    nbins = hist.GetBinsX()

    if direction == "above":
        running_content = hist.GetBinContent(nbins + 1)
        running_error2 = hist.GetBinError(nbins + 1)**2

        cumulative.SetBinContent(nbins + 1, running_content)
        cumulative.SetBinError(nbins + 1, math.sqrt(running_error2))

        for bin_idx in range(nbins, 0, -1):
            running_content += hist.GetBinContent(bin_idx)
            running_error2 += hist.GetBinError(bin_idx)**2
            cumulative.SetBinContent(bin_idx, running_content)
            cumulative.SetBinError(bin_idx, math.sqrt(running_error2))


        cumulative.SetBinContent(0, running_content + hist.GetBinContent(0))
        cumulative.SetBinError(0, math.sqrt(running_error2 + hist.GetBinError(0)**2))

        normalization = cumulative.GetBinContent(0)
        direction_text = "At or above threshold."

    else:
        running_content = hist.GetBinContent(0)
        running_error2 = hist.GetBinError(0)**2

        cumulative.SetBinContent(0)
        cumulative.GetBinError(0)**2

        for bin_idx in range(1, nbins + 1):
            running_content += hist.GetBinContent(bin_idx)
            running_error2 += hist.GetBinError(bin_idx)**2
            cumulative.SetBinContent(bin_idx, running_content)
            cumulative.SetBinError(bin_idx, math.sqrt(running_error2))


        cumulative.SetBinContent(nbins + 1, running_content + hist.GetBinContent(nbins + 1))
        cumulative.SetBinError(nbins + 1, math.sqrt(running_error2 + hist.GetBinError(nbins + 1)**2),)
        normalization = cumulative.GetBinContent(nbins + 1)
        direction_text = "At or above threshold."

    if normalize and normalization !=0.0:
        cumulative.Scale(1.0 / normalization)
        cumulative.GetYaxis().SetTitle("Cumulative fraction")
    else:
        cumulative.GetYaxis().SetTitle("Cumulative events")

    cumulative.SetTitle(f"{hist.GetTitle().split(';')[0]} ({direction_text})")

    cumulative.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())

    return cumulative

#Now, let's make a function to save our histograms in .ROOT files. We'll make one file per dataset/sample.
def save_histograms(histos, output_dir="histograms", cumulative_mode="scores", cumulative_direction="above", normalize_cumulative=False):
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

            if cumulative_flag(hist_name, cumulative_mode):
                cumulative_hist = make_cumulative_histogram(hist, direction=cumulative_direction, normalize=normalize_cumulative)
                cumulative_name = f"{hist_name}_cumulative"
                cumulative_hist.Write(cumulative_name)
                print(f"Wrote {cumulative_name} to {output_filename}")


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
    histos[sample_name] = book_histograms(
        rdf, sample_name, samples[sample_name]["label"], b_cuts
    )

#Finally, we'll save them.
save_histograms(histos, output_dir = "nBH_pt_cut_histograms", cumulative_mode = args.cumulative, cumulative_direction = args.cumulative_direction, normalize_cumulative = args.normalize_cumulative)



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

