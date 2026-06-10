import ROOT
import numpy as np
import os
import glob
from pathlib import Path

# Enable multi-threading
#ROOT.ROOT.EnableImplicitMT()





#-------------------------------------------------------------------------------#File load Module------------------------------------------------------------------------------------------#

#Input Directories

#Here is the parent directory with the NanoAOD files we need.
input_dir = [Path('/cms/data/store/user/hatake/ParTV2V3_Nanov15_v2')]

#Here is a list of all the subdirectories we may need for this analysis.
input_subdir = ['GluGluH-01J-HToAATo4B_Par-M-30_13p6TeV', 'GluGluH-01J-HToAATo4B_Par-M-35_13p6TeV', 'QCD0B-4Jets_Bin-HT-800to1000_Fil-BPS_13p6TeV', 'QCDB-4Jets_Bin-HT-800to1000_13p6TeV']


#Here is the pattern for the files that we will import.
nanoaod = ['Summer24NanoAODv15_*.root']


#ROOT files. Now let's build a consolidate the list of relevant directories.
analysis_list = [input_dir / input_subdir for directory in input_dir for subdir in input_subdir]


#Let's build some safety into this approach. We'll keep track of any directories that weare looking for but are missing. This may come in handy if our directory or subdirectory list ever gets long.
missing = [item for item in analysis_list if not item.isdir()]

for item in missing:
    print(f"{item} is missing.")

#Let's assemble the list of ROOT files.
rf_list = sorted({str(rootfile) for rdir in analysis_list for pattern in nanoaod for rootfile in rdir.glob(pattern)})


#Finally, let's send our list of files to ROOT.

#We'll include a test in case the list is huge.
# rf_list = rf_list[:40]

#Convert to a C++ vector<string>

#Initialize an empty c++ vector of strings
multi_file_vec = ROOT.std.vector("string")()

#fill the c++ vector with the rootfile names.
for rf in rf_list:
    multi_file_vec.push_back(rf)
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




#-----------------------------------------------------------------------------#Particle Transformer Module---------------------------------------------------------------------------------#

#Particle Transformer Module. We'll define ParT2 and ParT3 variables here. 

#Convert our c++ vector into RDataFrame
rdf = ROOT.RDataFrame("Events", multi_file_vec)









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
"""


columns = ["GenPart_pdgId","GenPart_status","GenPart_genPartIdxMother",
             "Higgs_GenFirst_pt","Higgs_GenFirst_phi","Higgs_GenFirst_eta","Higgs_GenFirst_mass","Higgs_GenLast_pt","Higgs_GenLast_phi","Higgs_GenLast_eta","Higgs_GenLast_mass"]

display = rdf.Display(columns,10)
#print(display.AsString())


#Apply Higgs Mask
#rdf_H_filtered = rdf_Higgs_Mask.Filter("ROOT::VecOps::Any(GenHiggsMask)")




#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Define C++ function to find specific GenParticles
# Here we find GenPart_pt of prompt leptons (status 1)
ROOT.gInterpreter.Declare("""
#include "ROOT/RVec.hxx"
#include <vector>

ROOT::RVecF getPromptLeptonPts(const ROOT::RVecF& pt, const ROOT::RVecI& status, const ROOT::RVecI& pdgId) {
    // Select prompt leptons (status 1, abs(pdgId) is 11 or 13)
    auto mask = (status == 1) && (abs(pdgId) == 11 || abs(pdgId) == 13);
    return pt[mask]; // Returns RVec of pts
}
""")


# Apply the function to the DataFrame
#rdf_with_pts = rdf.Define("PromptLepton_pt", "getPromptLeptonPts(GenPart_pt, GenPart_status, GenPart_pdgId)")

# Create a histogram of the result
#hist = rdf_with_pts.Histo1D(("PromptLepPt", "Prompt Lepton Pt;p_{T} [GeV];Events", 50, 0, 200), "PromptLepton_pt")
#hist.Draw()


#---------------------------------------------------------------------------#Gen-Level Histogram Module------------------------------------------------------------------------------------#

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
