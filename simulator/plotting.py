import csv
import matplotlib as mpl
import matplotlib.pyplot as plt

def scatter_plot(filename, lookup, xkey, ykey,
                 xlim = (0,1), ylim = (0,1)):
    x = lookup[xkey]
    y = lookup[ykey]

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


def plot_report(settings):
    output_settings = settings["output"]
    with open(output_settings["report"]) as f:
        reader = csv.DictReader(f, delimiter=";")
        results = [row for row in reader]

        column_values = lambda x: [float(row[x]) for row in results]
        lookup = {
            "effort": column_values("effort-norm"),
            "ddu": column_values("ddu"),
            "coverage": column_values("coverage"),
        }

        scatter_plot("output/coverage.pdf", lookup, "coverage", "effort")
        scatter_plot("output/coverage-ddu.pdf", lookup, "coverage", "ddu")
        scatter_plot("output/ddu.pdf", lookup, "ddu", "effort")
