import ROOT

# Enable multi-threading
ROOT.ROOT.EnableImplicitMT()

# Load NanoAOD file
rdf = ROOT.RDataFrame("Events", "/cms/data/store/mc/RunIII2024Summer24NanoAODv15/GluGluH-01J-HToAATo4B_Par-M-35_TuneCP5_13p6TeV_madgraph-pythia8/NANOAODSIM/150X_mcRun3_2024_realistic_v2-v2/2520000/0afb91ad-bf79-4830-ba1a-ebb5b2a0b4b4.root")

#-------------------------------------------------------------------------------

# 1. Define a mask for GenParticles that are electrons (pdgId 11)
# GenPart_pdgId is a vector branch, Define applies this per-event
rdf_with_mask = rdf.Define("GenElecMask", "abs(GenPart_pdgId) == 11")

# 2. Filter events: Keep only events where ANY electron passes the mask
rdf_filtered = rdf_with_mask.Filter("ROOT::VecOps::Any(GenElecMask)")

# 3. (Optional) Filter by pT: Keep events with electrons > 20 GeV
rdf_final = rdf_filtered.Filter("ROOT::VecOps::Any(GenPart_pt[GenElecMask] > 20)")

#-------------------------------------------------------------------------------

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
rdf_with_pts = rdf.Define("PromptLepton_pt", "getPromptLeptonPts(GenPart_pt, GenPart_status, GenPart_pdgId)")

# Create a histogram of the result
hist = rdf_with_pts.Histo1D(("PromptLepPt", "Prompt Lepton Pt;p_{T} [GeV];Events", 50, 0, 200), "PromptLepton_pt")
hist.Draw()

#-------------------------------------------------------------------------------

# Example 1: Select only GenParticles with status 1 and pt > 10 GeV
# GenPart_pt is typically a ROOT::RVec<float>
# rdf_gen = rdf.Filter("GenPart_status == 1 && GenPart_pt > 10.0")

# Example 2: Define a new column (e.g., Rapidity) using a lambda function
# The function acts on the whole RVec for each event
#rdf_with_rapidity = rdf_gen.Define("GenPart_rapidity",
#                                 "0.5 * log((sqrt(GenPart_mass*GenPart_mass + GenPart_pt*GenPart_pt*cosh(GenPart_eta)*cosh(GenPart_eta)) + GenPart_pt*sinh(GenPart_eta)) / (sqrt(GenPart_mass*GenPart_mass + GenPart_pt*GenPart_pt*cosh(GenPart_eta)*cosh(GenPart_eta)) - GenPart_pt*sinh(GenPart_eta)))")

# Example 3: Histogramming PT of specific GenParticles
#hist_gen_pt = rdf_with_rapidity.Histo1D(("gen_pt", "GenPart Pt;Pt [GeV];Counts", 100, 0, 100), "GenPart_pt")

#-------------------------------------------------------------------------------

# Save the histogram
outfile = ROOT.TFile("output.root", "RECREATE")
hist.Write()
#hist_gen_pt.Write()
outfile.Close()
