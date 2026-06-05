import ROOT
import os
import numpy as np

# Enable multi-threading
#ROOT.ROOT.EnableImplicitMT()

#Point the script to the ROOT files and enumerate the list so that we can analyze everything at once.
inDir = "/cms/data/store/user/hatake/ParTV2V3_Nanov15_v2/GluGluH-01J-HToAATo4B_Par-M-30_13p6TeV"
list_file = "FatJet_file_list.txt"

#Set up an empty list to store incoming filenames.
root_files = []

#Read the files into the root_file list
with open(list_file, "r") as f:
    for line in f:
        filename = line.strip()
        if filename == "":
            continue

        full_path = os.path.join(inDir, filename)
        root_files.append(full_path)

files_vec = ROOT.std.vector("string")()
for f in root_files:
    files_vec.push_back(f)

rdf = ROOT.RDataFrame("Events", files_vec)

#print("Total events:", rdf.Count().GetValue())


# Save the histogram
outfile = ROOT.TFile("HtoaaAna_FatJetn_HISTOS.root", "RECREATE")

