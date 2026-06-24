import ROOT
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os
import glob
from pathlib import Path

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


#Let's load the files we want to analyze.
def make_root_file_vector(file_list):
    files_vec = ROOT.std.vector("string")()

    for entry in file_list:
        files_vec.push_back(str(entry))

    return files_vec


def get_files_for_sample(parent_dir, sample_info, max_files=None):
    sample_dir = parent_dir / sample_info["subdir"]

    if not sample_dir.is_dir():
        print(f"Warning: missing directory: {sample_dir}")
        return []

    files = sorted(sample_dir.glob(sample_info["pattern"]))

    if max_files is not None:
        files = files[:max_files]

    return [str(f) for f in files]


#Make one RDataFrame per sample.
sample_files = {}
sample_rdf = {}

for sample_name, info in samples.items():
    files = get_files_for_sample(input_dir, info)

    sample_files[sample_name] = files

   # print(f"{sample_name}: found {len(files)} files")

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

ROOT::RVecI getHas4bScoreMask(const ROOT::RVecI& fatjet_genjet_idx,
                              const ROOT::RVecI& genjet_nBHadrons) {
    ROOT::RVecI mask(fatjet_genjet_idx.size(), 0);

    for (std::size_t i = 0; i < fatjet_genjet_idx.size(); ++i) {
        int idx = fatjet_genjet_idx[i];

        if (idx >= 0 && static_cast<std::size_t>(idx) < genjet_nBHadrons.size()) {
            if (genjet_nBHadrons[idx] >= 4) {
                mask[i] = 1;
            }
        }
    }

    return mask;
}
""")


#Let's set up a mask to make sure we only investigate events with some tagger score in the desired final state. "FatJet_pt > 300" getHas4bScoreMask(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons)")
def define_ParT_variables(rdf):

    #Define our nBhadrons mask using our helper function.
    rdf = rdf.Define("has4bScore", "getHas4bScoreMask(FatJet_genJetAK8Idx, GenJetAK8_nBHadrons)")

    #Define FatJet kinematics
    rdf = rdf.Define("FatJet_4b_pt", "FatJet_pt[has4bScore]")\
             .Define("FatJet_4b_eta", "FatJet_eta[has4bScore]")\
             .Define("FatJet_4b_msoftdrop", "FatJet_msoftdrop[has4bScore]")

    #Define FatJet Tagger Scores for on-shell ParT2 variables.
    rdf = rdf.Define("FatJet_4b_gl_ParT2_3b", "FatJet_globalParT2_probHZxZxbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT2_4b", "FatJet_globalParT2_probHZxZxbbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT2_b_channels","FatJet_4b_gl_ParT2_3b + FatJet_4b_gl_ParT2_4b")\
             .Define("FatJet_4b_gl_ParT2_QCD", "FatJet_globalParT2_probQCDb[has4bScore] + FatJet_globalParT2_probQCDbb[has4bScore] + FatJet_globalParT2_probQCDc[has4bScore] + FatJet_globalParT2_probQCDcc[has4bScore] + FatJet_globalParT2_probQCDothers[has4bScore]")\
             .Define("FatJet_4b_gl_ParT2_3b_Normed", "FatJet_4b_gl_ParT2_3b /(FatJet_4b_gl_ParT2_3b +  FatJet_4b_gl_ParT2_QCD)")\
             .Define("FatJet_4b_gl_ParT2_4b_Normed", "FatJet_4b_gl_ParT2_4b /(FatJet_4b_gl_ParT2_4b +  FatJet_4b_gl_ParT2_QCD)")\
             .Define("FatJet_4b_gl_ParT2_b_channels_Normed","FatJet_4b_gl_ParT2_b_channels / (FatJet_4b_gl_ParT2_b_channels + FatJet_4b_gl_ParT2_QCD)")
    
    #Define FatJet Tagger Scores for on-shell ParT3 variables.         
    rdf = rdf.Define("FatJet_4b_gl_ParT3_3b", "FatJet_globalParT3_probRawHZxZxbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT3_4b", "FatJet_globalParT3_probRawHZxZxbbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT3_b_channels","FatJet_4b_gl_ParT3_3b + FatJet_4b_gl_ParT3_4b")\
             .Define("FatJet_4b_gl_ParT3_QCD", "FatJet_globalParT3_QCD[has4bScore]")\
             .Define("FatJet_4b_gl_ParT3_3b_Normed", "FatJet_4b_gl_ParT3_3b /(FatJet_4b_gl_ParT3_3b +  FatJet_4b_gl_ParT3_QCD)")\
             .Define("FatJet_4b_gl_ParT3_4b_Normed", "FatJet_4b_gl_ParT3_4b /(FatJet_4b_gl_ParT3_4b +  FatJet_4b_gl_ParT3_QCD)")\
             .Define("FatJet_4b_gl_ParT3_b_channels_Normed","FatJet_4b_gl_ParT3_b_channels / (FatJet_4b_gl_ParT3_b_channels + FatJet_4b_gl_ParT3_QCD)")

    """
    #Define FatJet Tagger Scores for including off-shell ParT2 variables.
    rdf = rdf.Define("FatJet_4b_gl_ParT2_3b_adv1", "FatJet_globalParT2_probHZxZxStarbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT2_4b_adv1", "FatJet_globalParT2_probHZxZxStarbbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT2_b_channels_adv1","FatJet_4b_gl_ParT2_3b_adv1 + FatJet_4b_gl_ParT2_4b_adv1")\
             .Define("FatJet_4b_gl_ParT2_3b_adv1_Normed", "FatJet_4b_gl_ParT2_3b_adv1 /(FatJet_4b_gl_ParT2_3b_adv1 +  FatJet_4b_gl_ParT2_QCD)")\
             .Define("FatJet_4b_gl_ParT2_4b_adv1_Normed", "FatJet_4b_gl_ParT2_4b_adv1 /(FatJet_4b_gl_ParT2_4b_adv1 +  FatJet_4b_gl_ParT2_QCD)")\
             .Define("FatJet_4b_gl_ParT2_b_channels_adv1_Normed","FatJet_4b_gl_ParT2_b_channels / (FatJet_4b_gl_ParT2_b_channels_adv1 + FatJet_4b_gl_ParT2_QCD)")\
             .Define("FatJet_4b_gl_ParT2_3b_adv2", "FatJet_globalParT2_probHZZbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT2_4b_adv2", "FatJet_globalParT2_probHZZbbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT2_b_channels_adv2","FatJet_4b_gl_ParT2_3b_adv2 + FatJet_4b_gl_ParT2_4b_adv2")\
             .Define("FatJet_4b_gl_ParT2_3b_adv2_Normed", "FatJet_4b_gl_ParT2_3b_adv2 /(FatJet_4b_gl_ParT2_3b_adv2 +  FatJet_4b_gl_ParT2_QCD)")\
             .Define("FatJet_4b_gl_ParT2_4b_adv2_Normed", "FatJet_4b_gl_ParT2_4b_adv2 /(FatJet_4b_gl_ParT2_4b_adv2 +  FatJet_4b_gl_ParT2_QCD)")\
             .Define("FatJet_4b_gl_ParT2_b_channels_adv2_Normed","FatJet_4b_gl_ParT2_b_channels_adv2 / (FatJet_4b_gl_ParT2_b_channels_adv2 + FatJet_4b_gl_ParT2_QCD)")
         

    #Define FatJet Tagger Scores for including off-shell ParT3 variables.
    rdf = rdf.Define("FatJet_4b_gl_ParT3_3b_adv1", "FatJet_globalParT3_probRawHZxZxStarbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT3_4b_adv1", "FatJet_globalParT3_probRawHZxZxStarbbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT3_b_channels_adv1","FatJet_4b_gl_ParT3_3b_adv1 + FatJet_4b_gl_ParT3_4b_adv1")\
             .Define("FatJet_4b_gl_ParT3_3b_adv1_Normed", "FatJet_4b_gl_ParT3_3b_adv1 /(FatJet_4b_gl_ParT3_3b_adv1 +  FatJet_4b_gl_ParT3_QCD)")\
             .Define("FatJet_4b_gl_ParT3_4b_adv1_Normed", "FatJet_4b_gl_ParT3_4b_adv1 /(FatJet_4b_gl_ParT3_4b_adv1 +  FatJet_4b_gl_ParT3_QCD)")\
             .Define("FatJet_4b_gl_ParT3_b_channels_adv1_Normed","FatJet_4b_gl_ParT3_b_channels / (FatJet_4b_gl_ParT3_b_channels_adv1 + FatJet_4b_gl_ParT3_QCD)")\
             .Define("FatJet_4b_gl_ParT3_3b_adv2", "FatJet_globalParT3_probRawHZZbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT3_4b_adv2", "FatJet_globalParT3_probRawHZZbbbb[has4bScore]")\
             .Define("FatJet_4b_gl_ParT3_b_channels_adv2","FatJet_4b_gl_ParT3_3b_adv2 + FatJet_4b_gl_ParT3_4b_adv2")\
             .Define("FatJet_4b_gl_ParT3_3b_adv2_Normed", "FatJet_4b_gl_ParT3_3b_adv2 /(FatJet_4b_gl_ParT3_3b_adv2 +  FatJet_4b_gl_ParT3_QCD)")\
             .Define("FatJet_4b_gl_ParT3_4b_adv2_Normed", "FatJet_4b_gl_ParT3_4b_adv2 /(FatJet_4b_gl_ParT3_4b_adv2 +  FatJet_4b_gl_ParT3_QCD)")\
             .Define("FatJet_4b_gl_ParT3_b_channels_adv2_Normed","FatJet_4b_gl_ParT3_b_channels_adv2 / (FatJet_4b_gl_ParT3_b_channels_adv2 + FatJet_4b_gl_ParT3_QCD)")
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
#We'll define and save our FatJet histograms here.

def book_histograms(rdf, sample_name, label):
    histos = {}

    #Kinematics
    histos["pt"] = rdf.Histo1D((f"h_{sample_name}_FatJet_4b_pt", f"{label};FatJet p_{{T}} [GeV];Events", 100, 100., 1000.), "FatJet_4b_pt")
    histos["eta"] = rdf.Histo1D((f"h_{sample_name}_FatJet_4b_eta", f"{label};FatJet #eta;Events", 100, -7., 7.), "FatJet_4b_eta")
    histos["msoftdrop"] = rdf.Histo1D((f"h_{sample_name}_FatJet_4b_msoftdrop", f"{label};Soft drop mass [GeV];Events", 100, 20., 120.), "FatJet_4b_msoftdrop")
    
    #On-Shell Tagger Scores
    histos["ParT2_3b"] = rdf.Histo1D((f"h_{sample_name}_ParT2_3b", f"{label};ParT2 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_4b_gl_ParT2_3b_Normed")
    histos["ParT2_4b"] = rdf.Histo1D((f"h_{sample_name}_ParT2_4b", f"{label};ParT2 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_4b_gl_ParT2_4b_Normed")
    histos["ParT2_b_channels"] = rdf.Histo1D((f"h_{sample_name}_ParT2_b_channels", f"{label};ParT2 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_4b_gl_ParT2_b_channels_Normed")
    histos["ParT3_3b"] = rdf.Histo1D((f"h_{sample_name}_ParT3_3b", f"{label};ParT3 bbb / (bbb + QCD);Events", 100, 0., 1.), "FatJet_4b_gl_ParT3_3b_Normed")
    histos["ParT3_4b"] = rdf.Histo1D((f"h_{sample_name}_ParT3_4b", f"{label};ParT3 bbbb / (bbbb + QCD);Events", 100, 0., 1.), "FatJet_4b_gl_ParT3_4b_Normed")
    histos["ParT3_b_channels"] = rdf.Histo1D((f"h_{sample_name}_ParT3_b_channels", f"{label};ParT3 3b + 4b / (3b + 4b + QCD);Events", 100, 0., 1.),"FatJet_4b_gl_ParT3_b_channels_Normed")
    

    return histos






"""
#Additional Histograms including Off-Shell Z and Z*. ParT2 Type 1 and Type 2.
h_FatJet_4b_ParT2_3b_1 = rdf.Histo1D(("FatJet_4b_ParT2_3b_1", "FatJet HtoAAto4b Tagger Score (ZZ*); ParT2 bbb v QCD; Events", 100, 0., 1.), "FatJet_4b_gl_ParT2_3b_adv1")
h_FatJet_4b_ParT2_4b_1 = rdf.Histo1D(("FatJet_4b_ParT2_4b_1", "FatJet HtoAAto4b Tagger Score (ZZ*); ParT2 bbbb v QCD; Events", 100, 0., 1.), "FatJet_4b_gl_ParT2_4b_adv1")
h_FatJet_4b_ParT2_3b_2 = rdf.Histo1D(("FatJet_4b_ParT2_3b_2", "FatJet HtoAAto4b Tagger Score (ZZ); ParT2 bbb v QCD; Events", 100, 0., 1.), "FatJet_4b_gl_ParT2_3b_adv2")
h_FatJet_4b_ParT2_4b_2 = rdf.Histo1D(("FatJet_4b_ParT2_4b_2", "FatJet HtoAAto4b Tagger Score (ZZ); ParT2 bbbb v QCD; Events", 100, 0., 1.), "FatJet_4b_gl_ParT2_4b_adv2")

#Additional Histograms including Off-Shell Z and Z*. ParT3 Type 1 and Type 2.
h_FatJet_4b_ParT3_3b_1 = rdf.Histo1D(("FatJet_4b_ParT3_3b_1", "FatJet HtoAAto4b Tagger Score (ZZ*); ParT3 bbb v QCD; Events", 100, 0., 1.), "FatJet_4b_gl_ParT3_3b_adv1")
h_FatJet_4b_ParT3_4b_1 = rdf.Histo1D(("FatJet_4b_ParT3_4b_1", "FatJet HtoAAto4b Tagger Score (ZZ*); ParT3 bbbb v QCD; Events", 100, 0., 1.), "FatJet_4b_gl_ParT3_4b_adv1")
h_FatJet_4b_ParT3_3b_2 = rdf.Histo1D(("FatJet_4b_ParT3_3b_2", "FatJet HtoAAto4b Tagger Score (ZZ); ParT3 bbb v QCD; Events", 100, 0., 1.), "FatJet_4b_gl_ParT3_3b_adv2")
h_FatJet_4b_ParT3_4b_2 = rdf.Histo1D(("FatJet_4b_ParT3_4b_2", "FatJet HtoAAto4b Tagger Score (ZZ); ParT3 bbbb v QCD; Events", 100, 0., 1.), "FatJet_4b_gl_ParT3_4b_adv2")
"""

histos = {}

for sample_name, rdf in rdf_defined.items():
    histos[sample_name] = book_histograms(
        rdf,
        sample_name,
        samples[sample_name]["label"]
    )


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
#--------------------------------------------------------------------------------------------------------------------------------------#Matplotlib Plotting Module----------------------------------------------------------------------------------------------------------------------------------------------#

#We want to plot our variables using Matplotlib instead of the TCanvas protocol.

#Convert TH1D to np.
def th1_to_np(hist):
    
    nbins = hist.GetNbinsX()
    edges = np.array([hist.GetBinLowEdge(i) for i in range(1, nbins + 2)], dtype=float)
    contents = np.array([hist.GetBinContent(i) for i in range(1, nbins + 1)], dtype=float)
    errors = np.array([hist.GetBinError(i) for i in range(1, nbins + 1)], dtype=float)

    return edges, contents, errors


#Plot a single histogram
def single_hist_plotter(histogram, label, xlabel, title, output_name):
    hist = histogram.GetValue()

    edges, counts, errors = th1_to_np(hist)
    entries = hist.GetEntries()

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.stairs(counts, edges, label=label)

    ax.set_yscale("log")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Events")
    ax.set_title(title)
    ax.legend()

    ax.text(
        0.95,
        0.95,
        f"Entries = {int(entries)}",
        transform=ax.transAxes,
        ha="right",
        va="top"
    )

    fig.tight_layout()
    fig.savefig(output_name, dpi=300)
    plt.close(fig)


#Combine or overlay histograms for comparison.
def plot_overlay(histos, samples, sample_names, hist_name, xlabel, title, output_name, normalize=False):
    fig, ax = plt.subplots(figsize=(7, 5))

    for sample_name in sample_names:
        hist = histos[sample_name][hist_name].GetValue()

        edges, counts, errors = th1_to_np(hist)

        if normalize and counts.sum() > 0:
            counts = counts / counts.sum()

        ax.stairs(
            counts,
            edges,
            label=samples[sample_name]["label"]
        )

    ax.set_yscale("log")
    ax.set_xlabel(xlabel)

    if normalize:
        ax.set_ylabel("Normalized entries")
    else:
        ax.set_ylabel("Events")

    ax.set_title(title)
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_name, dpi=300)
    plt.close(fig)








plot_overlay(
    histos=histos,
    samples=samples,
    sample_names=["M30", "QCDB"],
    hist_name="ParT2_b_channels",
    xlabel="ParT2 3b + 4b v QCD",
    title="ParT2 score comparison",
    output_name="overlay_ParT2_b_channels.png",
    normalize=False
)
