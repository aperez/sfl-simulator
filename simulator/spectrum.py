from simulator.spectrum_filter import *

import sys

class Spectrum:

    def __init__(self):
        self.matrix = []
        self.transactions = 0
        self.components = 0

    def read(self, filename):
        f = open(filename)
        self.matrix = []
        for line in f:
            line = line.rstrip().replace(' ', '') \
                                .replace('x', '1')\
                                .replace('.', '0')\
                                .replace('-', '1')\
                                .replace('+', '0')
            line = map(int, line)
            self.matrix.append(line)

        self.calculate_dimensions()

    def append_transaction(self, transaction):
        self.matrix.append(transaction)

    def calculate_dimensions(self):
        self.transactions = len(self.matrix)
        self.components = len(self.matrix[0]) - 1

    def get_transaction_activity(self, transaction):
        return self.matrix[transaction]

    def get_activity(self, transaction, component):
        return self.matrix[transaction][component]

    def is_error(self, transaction):
        return self.matrix[transaction][-1]

    def print_spectrum(self, out=sys.stdout, spectrum_filter=None):
        if not spectrum_filter:
            spectrum_filter = SpectrumFilter(self)

        for t in spectrum_filter.transactions_filter:

            for c in spectrum_filter.components_filter:
                out.write('%d ' % self.get_activity(t, c))

            if self.is_error(t):
                out.write('x\n')
            else:
                out.write('.\n')
