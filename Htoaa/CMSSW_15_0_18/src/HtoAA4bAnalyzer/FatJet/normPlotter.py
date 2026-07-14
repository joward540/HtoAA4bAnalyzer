import argparse
import re
from pathlib import Path
import ROOT
import numpy as np
import matplotlib.pyplot as plt

ROOT.gROOT.SetBatch(True)

#Let's make a function to handle bad filenames that we may run into or accidentally generate. 
def clean_name(name):
    name = str(name)
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
    return name.strip("_")

#Let's generate  our plot filenames from our histogram filenames.
def sample_name_from_file(path):
    stem = Path(path).stem

    prefixes = ["FatJet_Histograms_", "Histograms_", "histograms_", "test_histograms", "test_histgrams_2", "combined_histograms", "nBHad0_histgrams", "nBHad1_histograms", "nBHad2_histograms", "nBHad4_histograms", "nBHadron_cut_histograms"]

    for prefix in prefixes:
        if stem.startswith(prefix):
            return stem[len(prefix):]

    return stem


#We want to handle histograms of n-dimensions using a single plotter.
def hist_dimension(obj):
    if not obj:
        return None

    # TH2 and TH3 inherit from TH1, so check higher dimensions first.
    if obj.InheritsFrom("TH3"):
        return 3
    if obj.InheritsFrom("TH2"):
        return 2
    if obj.InheritsFrom("TH1"):
        return 1

    return None

#We'll need to convert ROOT histograms to numpy objects.

def th1_to_np(hist):
    nbins = hist.GetNbinsX()

    edges = np.array([hist.GetBinLowEdge(i) for i in range(1, nbins + 2)], dtype=float)

    counts = np.array([hist.GetBinContent(i) for i in range(1, nbins + 1)], dtype=float)

    errors = np.array([hist.GetBinError(i) for i in range(1, nbins + 1)], dtype=float)

    integral = hist.Integral()

    normed_weights = counts / integral

    return edges, counts, errors, normed_weights

def th2_to_np(hist):
    nx = hist.GetNbinsX()
    ny = hist.GetNbinsY()

    xedges = np.array([hist.GetXaxis().GetBinLowEdge(i) for i in range(1, nx + 2)], dtype=float)

    yedges = np.array([hist.GetYaxis().GetBinLowEdge(i) for i in range(1, ny + 2)], dtype=float)

    counts = np.array([[hist.GetBinContent(ix, iy) for iy in range(1, ny + 1)] for ix in range(1, nx + 1)], dtype=float)

    return xedges, yedges, counts


#Here's how we'll handle our plot style.
def axis_title(axis, fallback):
    title = axis.GetTitle()
    if title:
        return title
    return fallback

def hist_label(hist, fallback):
    title = hist.GetTitle()
    if title:
        return title
    return fallback


#This is how we'll read our histograms in.
def read_histograms(hist_dirs, requested_hists=None, requested_dim="1", requested_samples=None):
    requested_hists = set(requested_hists) if requested_hists else None
    requested_samples = set(requested_samples) if requested_samples else None

    if requested_dim == "all":
        allowed_dims = {1, 2, 3}
    else:
        allowed_dims = {int(requested_dim)}
    
    histos = {}
    
    
    for hist_dir in hist_dirs:
        hist_dir = Path(hist_dir)
        dir_label = hist_dir.name

        if not hist_dir.exists():
            raise FileNotFoundError(f"Histogram directory does not exist: {hist_dir}")

        root_files = sorted(hist_dir.glob("*.root"))

        if not root_files:
            raise FileNotFoundError(f"No .root files found in: {hist_dir}")
        
        
        for root_path in root_files:
            sample_name = sample_name_from_file(root_path)
        
            if requested_samples and sample_name not in requested_samples:
                continue

            plot_label=f"{dir_label}:{sample_name}"

            f = ROOT.TFile.Open(str(root_path), "READ")

            if not f or f.IsZombie():
                print(f"Skipping unreadable file: {root_path}")
                continue

            histos[plot_label] = {}

            for key in f.GetListOfKeys():
                obj = key.ReadObj()
                name = key.GetName()

                if requested_hists and name not in requested_hists:
                    continue

                dim = hist_dimension(obj)

                if dim not in allowed_dims:
                    continue

                hist = obj.Clone(f"{clean_name(plot_label)}_{name}")
                hist.SetDirectory(0)

                histos[plot_label][name] = {
                    "hist": hist,
                    "dim": dim,
                    "source": root_path,
                }

            f.Close()

    histos = {
        sample: sample_histos
        for sample, sample_histos in histos.items()
        if sample_histos
    }

    return histos


#This is how we'll make our plots. 
def plot_1d(hist, sample_name, hist_name, output_path):
    edges, counts, _, normed_weights = th1_to_np(hist)
    entries = hist.GetEntries()

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.stairs(normed_weights, edges, label=hist_label(hist, sample_name))

    ax.set_yscale("log")
    ax.set_xlabel(axis_title(hist.GetXaxis(), hist_name))
    ax.set_ylabel("Events")
    ax.set_title(f"{sample_name}: {hist_name}")
    ax.legend()

    ax.text(0.95, 0.75, f"Entries = {int(entries)}", transform=ax.transAxes, ha="right", va="top")

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

def plot_2d(hist, sample_name, hist_name, output_path):
    xedges, yedges, counts = th2_to_np(hist)
    xlabel = hist.GetXaxis().GetTitle()
    ylabel = hist.GetYaxis().GetTitle()

    fig, ax = plt.subplots(figsize=(7, 5))

    hist_image = ax.pcolormesh(xedges, yedges, counts.T)
    fig.colorbar(hist_image, ax=ax, label="Events")

    if xlabel:
        ax.set_xlabel(xlabel)

    if ylabel:
        ax.set_ylabel(ylabel)
    
    ax.set_title(hist_name)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

def plot_individual(histos, plot_dir):
    plot_dir = Path(plot_dir)
    individual_dir = plot_dir / "individual"
    individual_dir.mkdir(parents=True, exist_ok=True)

    for sample_name, sample_histos in histos.items():
        for hist_name, record in sample_histos.items():
            hist = record["hist"]
            dim = record["dim"]

            output_name = (
                individual_dir
                / f"{clean_name(sample_name)}_{clean_name(hist_name)}.png"
            )

            if dim == 1:
                plot_1d(hist, sample_name, hist_name, output_name)
            elif dim == 2:
                plot_2d(hist, sample_name, hist_name, output_name)
            else:
                print(f"Skipping unsupported TH{dim}: {sample_name} {hist_name}")

def plot_overlay_1d(histos, plot_dir):
    overlay_dir = Path(plot_dir) / "overlays"
    overlay_dir.mkdir(parents=True, exist_ok=True)

    hist_names = sorted(
        {
            hist_name
            for sample_histos in histos.values()
            for hist_name, record in sample_histos.items()
            if record["dim"] == 1
        }
    )

    for hist_name in hist_names:
        fig, ax = plt.subplots(figsize=(7, 5))

        hist_list = []

        for sample_name, sample_histos in histos.items():
            if hist_name not in sample_histos:
                continue

            record = sample_histos[hist_name]

            if record["dim"] != 1:
                continue

            hist_list.append((sample_name, record["hist"]))

        if not hist_list:
            plt.close(fig)
            continue

        for sample_name, hist in hist_list:
            edges, counts, _, normed_weights = th1_to_np(hist)
            ax.stairs(normed_weights, edges, label=sample_name)

        xlabel = hist_list[0][1].GetXaxis().GetTitle()

        if xlabel:
            ax.set_xlabel(xlabel)

        ax.set_yscale("log")
        ax.set_ylabel("Events")
        ax.set_title(f"{hist_name} (Normalized)")
        ax.legend()

        fig.tight_layout()

        sample_names = [sample_name for sample_name, _ in hist_list]
        sample_tag = "_vs_".join(clean_name(name) for name in sample_names)

        output_name = overlay_dir / f"overlay_{sample_tag}_{clean_name(hist_name)}.png"

        #output_name = overlay_dir / f"overlay_{clean_name(sample_name)}_{clean_name(hist_name)}.png"
        fig.savefig(output_name, dpi=300)
        plt.close(fig)



def plot_1d_comparison(histos, plot_dir):
    compare_dir = Path(plot_dir) / "comparisons"
    compare_dir.mkdir(parents=True, exist_ok=True)

    for sample_name, sample_histos in histos.items():

        hist_list = []

        # Build the list first
        for hist_name, record in sample_histos.items():
            if record["dim"] != 1:
                continue

            hist_list.append((hist_name, record["hist"]))

        if len(hist_list) < 2:
            continue

        # Optional: put uncut first and _cut second
        hist_list = sorted(hist_list, key=lambda x: x[0].endswith("_cut"))

        fig, ax = plt.subplots(figsize=(7, 5))

        for hist_name, hist in hist_list:
            edges, counts, _, normed_weights = th1_to_np(hist)

            if hist_name.endswith("_cut"):
                linestyle = "--"
                linewidth = 2.5
                zorder = 3
            else:
                linestyle = "-"
                linewidth = 2.0
                zorder = 2

            ax.stairs(
                normed_weights,
                edges,
                label=hist_name,
                fill=False,
                linestyle=linestyle,
                linewidth=linewidth,
                zorder=zorder
            )

        xlabel = hist_list[0][1].GetXaxis().GetTitle()

        if xlabel:
            ax.set_xlabel(xlabel)

        ax.set_yscale("log")
        ax.set_ylabel("Events")
        ax.set_title(f"{sample_name}: histogram comparison")
        ax.legend()

        fig.tight_layout()

        compared_names = "_vs_".join(clean_name(name) for name, _ in hist_list)
        output_name = compare_dir / f"compare_{clean_name(sample_name)}_{compared_names}.png"

        fig.savefig(output_name, dpi=300)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Plot ROOT histograms from a directory of .root files.")

    parser.add_argument("--hist-dir", default="histograms", help="Directory containing ROOT histogram files.")
    parser.add_argument("--hist-dirs", nargs="+", default=None, help="Directories containing ROOT histogram files.")
    parser.add_argument("--plot-dir", default="plots", help="Directory where plots will be written.")
    parser.add_argument("--hists", nargs="+", default=None, help="Optional list of histogram names to plot.")
    parser.add_argument("--samples", nargs="+", default=None, help="Optional list of sample names to plot.")
    parser.add_argument("--mode", choices=["individual", "overlay", "compare", "both"], default="both", help="Choose individual plots, overlays (multiple samples), comparison (same sample), or both.")
    parser.add_argument("--dim", choices=["1", "2", "all"], default="1", help="Histogram dimension to plot. Default is 1.")

    args = parser.parse_args()

    if args.hist_dirs is not None:
        hist_dirs = args.hist_dirs
    else:
        hist_dirs = [args.hist_dir]

        
    histos = read_histograms(hist_dirs=hist_dirs, requested_hists=args.hists, requested_dim=args.dim, requested_samples=args.samples)

    if not histos:
        print("No matching histograms found.")
        return

    if args.mode in ["individual", "both"]:
        plot_individual(histos, args.plot_dir)

    if args.mode in ["overlay", "both"]:
        plot_overlay_1d(histos, args.plot_dir)

    if args.mode == "compare":
        plot_1d_comparison(histos, args.plot_dir)

    print(f"Plots written to: {args.plot_dir}")


if __name__ == "__main__":
    main()
