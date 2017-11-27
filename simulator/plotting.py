import csv
import operator
import itertools
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats
import glob2

from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def scatter_plot(filename, lookup, xkey, ykey,
                 xlim = (0,1), ylim = (0,1), correlation=False):
    x = lookup[xkey]
    y = lookup[ykey]

    # remove duplicate points
    decimal_points = 2
    point_set = set(zip(x,y))
    x = [round(px, decimal_points) for px,_ in point_set]
    y = [round(py, decimal_points) for _,py in point_set]

    fig, ax = plt.subplots()
    plt.scatter(x, y, s=3)

    if correlation:
        fit = np.polyfit(x, y, deg=1)
        plt.plot(x, fit[0] * np.array(x) + fit[1], color='red')

    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)

    plt.xlabel(xkey)
    plt.ylabel(ykey)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight")

def hist2d_plot(filename, lookup, xkey, ykey,
                xlim = (0,1), ylim = (0,0.8), correlation=False):
    x = lookup[xkey]
    y = lookup[ykey]

    #colormap
    colors = [(0.85, 0.85, 0.85),(0.20, 0.20, 0.20)]
    cm = LinearSegmentedColormap.from_list("my_cmap", colors, N=50)

    fig, ax = plt.subplots()
    plt.hist2d(x,y,bins=75,range=[xlim,ylim],vmin=0,vmax=200,cmin=0.001,cmap=cm)

    if correlation:
        fit = np.polyfit(x, y, deg=1)
        plt.plot(x, fit[0] * np.array(x) + fit[1], color='red')

    # plt.xlabel(xkey)
    plt.ylabel(ykey)

    cbaxes = inset_axes(ax, width="30%", height="3%", loc=1, borderpad=1)
    plt.colorbar(cax=cbaxes, ticks=[0.,200], orientation='horizontal')

    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)

    plt.tight_layout()
    plt.savefig(filename)

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

    lookup = {
        "Effort": column_values("effort-norm"),
        "DDU": column_values("ddu"),
        "Coverage": column_values("coverage"),
        "density": density_values,
        "diversity": diversity_values,
        "uniqueness": uniqueness_values,
        "ddu-avg": ddu_avg_values,
        "Entropy": column_values("entropy"),
        "error-detection": column_values("error-detection")
    }

    hist2d_plot("output/coverage-h.pdf", lookup, "Coverage", "Effort")
    hist2d_plot("output/ddu-h.pdf", lookup, "DDU", "Effort")
    hist2d_plot("output/entropy-h.pdf", lookup, "Entropy", "Effort")
    hist2d_plot("output/ddu-avg-h.pdf", lookup, "ddu-avg", "Effort")
