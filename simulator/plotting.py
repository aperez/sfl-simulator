import csv
import matplotlib as mpl
import matplotlib.pyplot as plt

def scatter_plot(filename, x, y,
                 xlim = (0,1), ylim = (0,1)):
    fig, ax = plt.subplots()
    plt.scatter(x, y)

    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight")


def plot_report(report_path):
    with open(report_path) as f:
        reader = csv.DictReader(f, delimiter=";")
        results = [row for row in reader]

        column_values = lambda x: [float(row[x]) for row in results]
        lookup = {
            "effort": column_values("effort"),
            "ddu": column_values("ddu"),
            "coverage": column_values("coverage"),
        }

        effort_values = lookup["effort"]

        scatter_plot("output/coverage.pdf", lookup["coverage"], effort_values,
                     ylim = (0, max(effort_values) + 1))

        scatter_plot("output/coverage-ddu.pdf", lookup["coverage"], lookup["ddu"])

        scatter_plot("output/ddu.pdf", lookup["ddu"], effort_values,
                     ylim = (0, max(effort_values) + 1))
