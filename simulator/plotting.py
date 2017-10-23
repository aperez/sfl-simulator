import csv
import operator
import itertools
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats

def scatter_plot(filename, lookup, xkey, ykey,
                 xlim = (0,1), ylim = (0,1), correlation=False):
    x = lookup[xkey]
    y = lookup[ykey]

    # remove duplicate points
    decimal_points = 3
    point_set = set(zip(x,y))
    x = [round(px, decimal_points) for px,_ in point_set]
    y = [round(py, decimal_points) for _,py in point_set]

    fig, ax = plt.subplots()
    plt.scatter(x, y, s=4)

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
    files = [settings["report"]]
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
        "effort-norm": column_values("effort-norm"),
        "ddu": column_values("ddu"),
        "coverage": column_values("coverage"),
        "density": density_values,
        "diversity": diversity_values,
        "uniqueness": uniqueness_values,
        "ddu-avg": ddu_avg_values,
        "entropy": column_values("entropy"),
        "error-detection": column_values("error-detection")
    }

    #print(scipy.stats.pearsonr(lookup["coverage"], lookup["effort-norm"]))
    #print(scipy.stats.pearsonr(lookup["ddu"], lookup["effort-norm"]))

    scatter_plot("output/coverage.pdf", lookup, "coverage", "effort-norm")
    scatter_plot("output/coverage-ddu.pdf", lookup, "coverage", "ddu")
    scatter_plot("output/ddu.pdf", lookup, "ddu", "effort-norm")

    scatter_plot("output/density.pdf", lookup, "density", "effort-norm")
    scatter_plot("output/diversity.pdf", lookup, "diversity", "effort-norm")
    scatter_plot("output/uniqueness.pdf", lookup, "uniqueness", "effort-norm")

    scatter_plot("output/ddu-avg.pdf", lookup, "ddu-avg", "effort-norm")
    scatter_plot("output/entropy.pdf", lookup, "entropy", "effort-norm")

    scatter_plot("output/detection-ddu.pdf", lookup, "ddu", "error-detection")
    scatter_plot("output/detection-coverage.pdf",
                 lookup, "coverage", "error-detection")
