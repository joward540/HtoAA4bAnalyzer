import root
import numpy as np
import matplotlib.pyplot as plt



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
    ax.text(0.95, 0.75, f"Entries = {int(entries)}", transform=ax.transAxes, ha="right", va="top")
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

        ax.stairs(counts, edges, label=samples[sample_name]["label"])
    
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




#---------------------------------------------------------------------------------------------------Main----------------------------------------------------------------------------------------------------#

single_hist_plotter(
    histos["QCD0B"]["ParT3_3b"],
    samples["QCD0B"]["label"],
    "Test ParT3 bbb / (bbb + QCD) (GenJetAK8_nBHadrons >= 0)",
    "FatJet HtoAAto4b QCD0B HT 800-1000",
    "Test_5_QCD0B_ParT3_3b.png"
)
"""

plot_overlay(
    histos=histos,
    samples=samples,
    sample_names=["M30", "M35", "QCDB", "QCD0B"],
    hist_name="ParT3_3b",
    xlabel="ParT3 bbb / (bbb + QCD)",
    title="ParT3 M30 v M35 v QCDB v QCD0B",
    output_name="overlay_ParT3_3b_all_datasets.png",
    normalize=False
)


plot_dir = Path("plots")
plot_dir.mkdir(exist_ok=True)

signals = ["M30", "M35"]
backgrounds = ["QCD0B", "QCDB"]
all_samples = signals + backgrounds

hist_names = [
    "ParT2_3b",
    "ParT2_4b",
    "ParT2_b_channels",
    "ParT3_3b",
    "ParT3_4b",
    "ParT3_b_channels",
]

hist_xlabels = {
    "ParT2_3b": "ParT2 bbb v QCD",
    "ParT2_4b": "ParT2 bbbb v QCD",
    "ParT2_b_channels": "ParT2 3b + 4b v QCD",
    "ParT3_3b": "ParT3 bbb v QCD",
    "ParT3_4b": "ParT3 bbbb v QCD",
    "ParT3_b_channels": "ParT3 3b + 4b v QCD",
}


# Make individual plots for every sample.
for hist_name in hist_names:
    for sample_name in all_samples:

        if sample_name not in histos:
            #print(f"Skipping {sample_name}: no histograms found")
            continue

        if hist_name not in histos[sample_name]:
            #print(f"Skipping {sample_name} {hist_name}: histogram not found")
            continue

        output_name = plot_dir / f"{sample_name}_{hist_name}.png"

       single_hist_plotter(
            histogram=histos[sample_name][hist_name],
            label=samples[sample_name]["label"],
            xlabel=hist_xlabels[hist_name],
            title=f"{samples[sample_name]['label']} {hist_name}",
            output_name=str(output_name)
        )

# Plot all signals vs all backgrounds.
for hist_name in hist_names:
    for signal_name in signals:
        for background_name in backgrounds:

            sample_pair = [signal_name, background_name]

            # Safety check
            missing = [
                sample_name for sample_name in sample_pair
                if sample_name not in histos or hist_name not in histos[sample_name]
            ]

            if missing:
                #print(f"Skipping overlay {hist_name} for {sample_pair}. Missing: {missing}")
                continue

            output_name = plot_dir / f"overlay_{signal_name}_vs_{background_name}_{hist_name}.png"

            plot_overlay(
                histos=histos,
                samples=samples,
                sample_names=sample_pair,
                hist_name=hist_name,
                xlabel=hist_xlabels[hist_name],
                title=f"{hist_name}: {signal_name} vs {background_name}",
                output_name=str(output_name),
                normalize=False
            )
"""


