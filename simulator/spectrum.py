from simulator.spectrum_filter import *

import sys
import random

class Spectrum(object):

    def __init__(self):
        self.matrix = []
        self.transactions = 0
        self.components = 0
        self.faults = []
        self.id = None

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

    def failing_transaction_count(self):
        return sum([1 for t in self.matrix if t[-1] == 1])

    def print_spectrum(self, out=sys.stdout, spectrum_filter=None):
        if not spectrum_filter:
            spectrum_filter = SpectrumFilter(self)

        for t in spectrum_filter.transactions_filter:

            for c in spectrum_filter.components_filter:
                out.write('%d ' % self.get_activity(t, c))

            if self.is_error(t):
                out.write('-\n')
            else:
                out.write('+\n')
        #out.write(str(self.faults)+'\n')

    def sample_spectra(self, num_samples, num_transactions=None, seed=None):
        if num_transactions is None:
            num_transactions = self.components

        if seed is not None:
            random.seed(seed)

        samples = []
        for _ in range(num_samples):
            s = Spectrum()
            s.matrix = [t[:] for t in
                        random.sample(self.matrix, num_transactions)]
            s.calculate_dimensions()
            samples.append(s)

        return samples

    def copy(self):
        s = Spectrum()
        s.id = self.id
        s.matrix = [t[:] for t in self.matrix]
        s.faults = self.faults[:]
        s.calculate_dimensions()
        return s

    def inject_fault(self, faults=None, cardinality=1, goodness=0, seed=None):
        if seed is not None:
            random.seed(seed)

        if faults is None:
            current_faults = [x for fault in self.faults for x in fault]
            potential_faults = [x for x in range(self.components)
                                if x not in current_faults]
            faults = random.sample(potential_faults, cardinality)

        for t in self.matrix:
            inject = True
            for f in faults:
                if f < self.components and t[f] == 0:
                    inject = False
                    break

            if inject and random.random() <= (1.0 - goodness):
                    t[-1] |= 1

        self.faults.append(faults)
        return faults

    def remove_components(self, ratio_range=[0.0, 1.0], seed=None):
        if seed is not None:
            random.seed(seed)

        ratio_range = [int(x * self.components) for x in ratio_range]
        to_remove = random.randint(*ratio_range)

        components_list = [x for x in range(self.components)]

        for c in random.sample(components_list, to_remove):
            for transaction in self.matrix:
                transaction[c] = 0;
