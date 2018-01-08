import csv
import operator
import itertools
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats
import glob2
import random

from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from matplotlib import rcParams
rcParams['axes.titlepad'] = 2.5

## Colors & Colormaps
col = lambda r,g,b: (r/255.0, g/255.0, b/255.0)
BLUE = col(0,51,102)
RED = col(227,0,0)
GREEN = col(50,138,46)

BLUES = [col(192,214,228), col(100,151,177), col(11,26,77)]
BLUES_CM = LinearSegmentedColormap.from_list("blues_cm", BLUES, N=8)

REDS = [col(255,133,133), col(255,71,71), col(255,0,0), col(103,0,0)]
REDS_CM = LinearSegmentedColormap.from_list("reds_cm", REDS, N=8)

GREENS = [col(141,207,138),col(90,172,86), col(50,138,46), col(21,103,17), col(3,69,0)]
GREENS_CM = LinearSegmentedColormap.from_list("greens_cm", GREENS, N=8)

HMAP = [col(29,72,119),col(27,138,90), col(251,176,33), col(246,136,56), col(238,62,50)]
HMAP_CM = LinearSegmentedColormap.from_list("hmap_cm", HMAP, N=2*len(HMAP))

def remove_duplicates(x, y, samples=5000):
    if len(x) < samples:
        samples = len(x)

    point_set = set(random.sample(list(zip(x, y)), samples))
    return [x for x,_ in point_set], [y for _, y in point_set]

def hist2d_ax(fig, ax, x, y, xlim, ylim, cm, vmin=0, vmax = 150, bins=35):
    h = ax.hist2d(x, y, bins=bins, range=[xlim, ylim], vmin=vmin, vmax=vmax, cmin=0.001, cmap=cm)

    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)

    cbar = fig.colorbar(h[3], ax=ax, ticks=[vmin, vmax])
    cbar.ax.tick_params(labelsize=6)

def scatter_plot(filename, lookup, xkey, ykey, xlim=(0,1), ylim=(0,1)):
    x = lookup[xkey]
    y = lookup[ykey]

    fts = lookup['fault-type']
    fts = list(zip(fts, x, y))
    x = [x for f, x, _ in fts if f == (1.0, 1.0)]
    y = [y for f, _, y in fts if f == (1.0, 1.0)]
    xr, yr = remove_duplicates(x, y)
    xi = [x for f, x, _ in fts if f[0] == 1.0 and f[1] != 1.0]
    yi = [y for f, _, y in fts if f[0] == 1.0 and f[1] != 1.0]
    xir, yir = remove_duplicates(xi, yi)
    xd = [x for f, x, _ in fts if f[0] != 1.0]
    yd = [y for f, _, y in fts if f[0] != 1.0]
    xdr, ydr = remove_duplicates(xd, yd)

    fig = plt.figure(figsize=(10,4))
    ax1 = plt.subplot2grid((3,8), (0,0), colspan=6, rowspan=3)
    ax2 = plt.subplot2grid((3,8), (0,6), colspan=2)
    ax3 = plt.subplot2grid((3,8), (1,6), colspan=2, sharex = ax2)
    ax4 = plt.subplot2grid((3,8), (2,6), colspan=2, sharex = ax2)

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.15, wspace=.5)
    for ax in [ax2, ax3]:
        plt.setp(ax.get_xticklabels(), visible=False)

    for ax, visible in [(ax1, True), (ax2, False), (ax3, False), (ax4, True)]:
        plt.setp(ax.get_xticklabels(), fontsize=8, visible=visible)
        plt.setp(ax.get_yticklabels(), fontsize=8)

    ax1.scatter(xdr, ydr, s=9, label="Dependent Faults", c=RED, alpha=0.9)
    ax1.scatter(xir, yir, s=9, label="Independent Faults", c=GREEN, alpha=0.9)
    ax1.scatter(xr, yr, s=9, label="Single Faults", c=BLUE, alpha=0.9)

    hist2d_ax(fig, ax2, x, y, xlim, ylim, BLUES_CM)
    ax2.set_title("Single Faults", fontsize=9)

    hist2d_ax(fig, ax3, xi, yi, xlim, ylim, GREENS_CM)
    ax3.set_title("Independent Faults", fontsize=9)

    hist2d_ax(fig, ax4, xd, yd, xlim, ylim, REDS_CM)
    ax4.set_title("Dependent Faults", fontsize=9)

    if xlim:
        ax1.set_xlim(*xlim)
        ax2.set_xlim(*xlim)
    if ylim:
        ax1.set_ylim(*ylim)
        ax2.set_ylim(*ylim)

    handles, labels = ax1.get_legend_handles_labels()

    ax1.legend(handles[::-1], labels[::-1], fontsize=8)

    ax0 = fig.add_subplot(111, frame_on=False)
    ax0.set_xticks([])
    ax0.set_yticks([])
    ax0.set_xlabel(xkey, labelpad = 20)
    ax0.set_ylabel(ykey, labelpad = 25)

    plt.savefig(filename, bbox_inches="tight")

def ed_plot(filename, lookup, xkey, ykey, xlim = (0,1), ylim = (0,1), vmax=600, bins=25):
    x = lookup[xkey]
    y = lookup[ykey]

    xy = list(zip(x,y))
    x = [t[0] for t in xy]
    y = [t[1] for t in xy]

    fig = plt.figure(figsize=(5,4))
    _, ax = plt.subplots()
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.15, wspace=.5)

    h = ax.hist2d(x,y,bins=bins,range=[xlim,ylim],vmin=0,vmax=vmax,
                  cmin=0.001,cmap=HMAP_CM)

    plt.xlabel(xkey)
    plt.ylabel(ykey)
    plt.setp(ax.get_xticklabels(), fontsize=8)
    plt.setp(ax.get_yticklabels(), fontsize=8)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

    cbar = fig.colorbar(h[3], ax=ax, ticks=[0, vmax])
    cbar.ax.tick_params(labelsize=6)

    plt.savefig(filename, bbox_inches="tight")

def average_results(results):
    skip_keys = ["id", "components", "transactions", "faults", "cardinality"]
    item = None
    for row in results:
        if item is None:
            item = row
        else:
            new_item = {x: float(y) + float(item[x]) for x,y in row.items()
                        if x not in skip_keys}
            item.update(new_item)

    if item is None:
        return []
    else:
        results_len = len(results)
        reduced_item = {x: float(y) / results_len for x,y in item.items()
                        if x not in skip_keys}
        item.update(reduced_item)
        return [item]

def process_results(settings, results):
    processed = []
    for _, group in itertools.groupby(results,
                                      key=operator.itemgetter("id")):
        group = [x for x in group]
        group = average_results(group)
        processed.extend(group)
    return processed

def read_results(settings):
    results = []
    files = glob2.glob(settings["folder"] + "*.csv")
    id_offset = 0
    last_id = 0

    for fs in files:
        id_offset += last_id + 1
        with open(fs) as f:
            reader = csv.DictReader(f, delimiter=";")
            rs = [row for row in reader]
            for row in rs:
                row["error-detection"] = 1 if int(row.get("failing-transactions", 0)) > 0 else 0
                last_id = int(row["id"])
                row["id"] = last_id + id_offset
                row['deps'] = len(eval(row['faults'])[0])
        results.extend(rs)

    results = process_results(settings, results)
    return results

def plot_report(settings):
    output_settings = settings["output"]
    results = read_results(output_settings)

    column_values = lambda x: [float(row[x]) for row in results]
    density_values = column_values("density")
    diversity_values = column_values("diversity")
    uniqueness_values = column_values("uniqueness")

    ddu_avg_values = [(x+y+z)/3 for x,y,z in zip(density_values,
                                                 diversity_values,
                                                 uniqueness_values)]

    ed_selector = "Error Detection"
    avg_selector = "Average of Density, Diversity and Uniqueness"

    lookup = {
        "Effort": column_values("effort-norm"),
        "DDU": column_values("ddu"),
        "Coverage": column_values("coverage"),
        "density": density_values,
        "diversity": diversity_values,
        "uniqueness": uniqueness_values,
        avg_selector: ddu_avg_values,
        "Entropy": column_values("entropy"),
        "fault-type": list(zip(column_values('cardinality'), column_values('deps'))),
        ed_selector: column_values("error-detection"),
    }

    fname = lambda x: "{}/{}".format(output_settings["folder"], x)
    scatter_plot(fname("scatter-cov.pdf"), lookup, "Coverage", "Effort", ylim=(0,0.6))
    scatter_plot(fname("scatter-ddu.pdf"), lookup, "DDU", "Effort", ylim=(0,0.6))
    scatter_plot(fname("scatter-entropy.pdf"), lookup, "Entropy", "Effort", ylim=(0,0.6))
    scatter_plot(fname("scatter-ddu-avg.pdf"), lookup, avg_selector, "Effort", ylim=(0,0.6))

    ed_plot(fname("error-detection-ddu.pdf"), lookup, "DDU", ed_selector)
    ed_plot(fname("error-detection-coverage.pdf"), lookup, "Coverage", ed_selector)
