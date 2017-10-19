import csv
import operator
import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt

def scatter_plot(filename, lookup, xkey, ykey,
                 xlim = (0,1), ylim = (0,1)):
    x = lookup[xkey]
    y = lookup[ykey]

    # remove duplicate points
    point_set = set(zip(x,y))
    x = [px for px,_ in point_set]
    y = [py for _,py in point_set]

    fig, ax = plt.subplots()
    plt.scatter(x, y)

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

def plot_report(settings):
    output_settings = settings["output"]
    with open(output_settings["report"]) as f:
        reader = csv.DictReader(f, delimiter=";")
        results = [row for row in reader]
        results = process_results(output_settings, results)

        column_values = lambda x: [float(row[x]) for row in results]
        lookup = {
            "effort-norm": column_values("effort-norm"),
            "ddu": column_values("ddu"),
            "coverage": column_values("coverage"),
        }

        scatter_plot("output/coverage.pdf", lookup, "coverage", "effort-norm")
        scatter_plot("output/coverage-ddu.pdf", lookup, "coverage", "ddu")
        scatter_plot("output/ddu.pdf", lookup, "ddu", "effort-norm")
