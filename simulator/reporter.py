from .metrics import *
from .effort import *

import csv

class Reporter(object):

    def __init__(self, filename="output.csv"):
        self.filename = filename
        self.file = None
        self.csv = None
        self.fieldnames = ["id",
                           "components",
                           "transactions",
                           "faults",
                           "cardinality",
                           "coverage",
                           "density",
                           "diversity",
                           "uniqueness",
                           "ddu",
                           "entropy",
                           "effort",
                           "effort-norm",
                           "failing-transactions"]

    def __enter__(self):
        self.file = open(self.filename, 'w')
        self.csv = csv.DictWriter(self.file,
                                  delimiter=";",
                                  fieldnames=self.fieldnames)
        self.csv.writeheader()
        return self

    def write(self, spectrum, report):
        ddu_value, den, div, uniq = ddu(spectrum)
        effort_value = effort_reduced(spectrum, report)
        row = {"id": spectrum.id,
               "components": spectrum.components,
               "transactions": spectrum.transactions,
               "faults": str(spectrum.faults),
               "cardinality": len(spectrum.faults),
               "coverage": coverage(spectrum),
               "density": den,
               "diversity": div,
               "uniqueness": uniq,
               "ddu": ddu_value,
               "entropy": entropy(spectrum),
               "effort": effort_value,
               "effort-norm": effort_value / spectrum.components,
               "failing-transactions": spectrum.failing_transaction_count()}
        self.csv.writerow(row)

    def __exit__(self, type, value, traceback):
        self.file.close()
