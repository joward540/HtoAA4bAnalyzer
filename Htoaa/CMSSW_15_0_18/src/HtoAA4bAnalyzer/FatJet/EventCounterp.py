import ROOT
from pathlib import Path

base_directory = Path(
    "/cms/data/store/user/hatake/ParTV2V3_Nanov15_v2"
)

folders = {
    "QCD0B": "QCD0B-4Jets_Bin-HT-800to1000_Fil-BPS_13p6TeV",
    "QCDB":  "QCDB-4Jets_Bin-HT-800to1000_13p6TeV",
    "M35":   "GluGluH-01J-HToAATo4B_Par-M-35_13p6TeV",
    "M30":   "GluGluH-01J-HToAATo4B_Par-M-30_13p6TeV",
}

file_pattern = "Summer24NanoAODv15_*_13p6TeV_job*.root"

# Only apply the FatJet cut to these samples
signal_datasets = {"M30", "M35"}


def build_chain(dataset_name):
    """Build and return an Events TChain for one dataset."""

    if dataset_name not in folders:
        raise ValueError(
            f"Unknown dataset '{dataset_name}'. "
            f"Choose from: {list(folders)}"
        )

    dataset_directory = base_directory / folders[dataset_name]
    files = sorted(dataset_directory.glob(file_pattern))

    chain = ROOT.TChain("Events")

    for file_path in files:
        chain.Add(str(file_path))

    return chain, files


results = {}
chains = {}

# ------------------------------------------------------------
# First: count the total files and events in every dataset
# ------------------------------------------------------------

print("\nTotal event counts")
print(f"{'Dataset':<10} {'Files':>10} {'Total events':>20}")


for dataset_name in folders:
    chain, files = build_chain(dataset_name)

    number_of_files = len(files)
    total_events = chain.GetEntries()

    # Save these so that the signal calculation can reuse them
    chains[dataset_name] = chain
    results[dataset_name] = {
        "files": number_of_files,
        "total_events": total_events,
    }

    print(
        f"{dataset_name:<10} "
        f"{number_of_files:>10,d} "
        f"{total_events:>20,d}"
    )


# ------------------------------------------------------------
# Second: count signal events with at least one FatJet_pt > 150
# ------------------------------------------------------------

fatjet_cut = "Sum$(FatJet_pt > 150) > 0"

print("\nSignal event counts after FatJet_pt > 150 cut")
print(
    f"{'Dataset':<10} "
    f"{'Total events':>18} "
    f"{'Passing events':>18} "
    f"{'Pass ratio':>15}"
)

for dataset_name in ("M30", "M35"):
    chain = chains[dataset_name]
    total_events = results[dataset_name]["total_events"]

    passing_events = chain.GetEntries(fatjet_cut)

    if total_events > 0:
        pass_ratio = passing_events / total_events
    else:
        pass_ratio = 0.0

    results[dataset_name]["passing_events"] = passing_events
    results[dataset_name]["pass_ratio"] = pass_ratio

    print(
        f"{dataset_name:<10} "
        f"{total_events:>18,d} "
        f"{passing_events:>18,d} "
        f"{pass_ratio:>14.4}"
    )
