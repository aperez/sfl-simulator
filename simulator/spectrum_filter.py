import sys

class SpectrumFilter:

    def __init__(self, spectrum):
        if spectrum:
            self.transactions_filter = \
                [x for x in range(spectrum.transactions)]
            self.components_filter = \
                [x for x in range(spectrum.components)]

    def copy(self):
        sf = SpectrumFilter(None)
        sf.transactions_filter = self.transactions_filter[:]
        sf.components_filter = self.components_filter[:]
        return sf

    def strip_component(self, spectrum, component):
        self.transactions_filter = [t for t in self.transactions_filter
                                    if not spectrum.get_activity(t, component)]
        self.components_filter.remove(component)

    def filter_component(self, component):
        self.components_filter.remove(component)

    def filter_transaction(self, transaction):
        self.transactions_filter.remove(transaction)

    def filter_passing_transactions(self, spectrum):
        self.transactions_filter = [t for t in self.transactions_filter
                                    if spectrum.is_error(t)]

    def has_failing_transactions(self, spectrum):
        for t in self.transactions_filter:
            if spectrum.is_error(t):
                return True
        return False

    def print_filter(self, out=sys.stdout):
        out.write('Transactions:\t%s\n' % self.transactions_filter)
        out.write('Components:\t%s\n' % self.components_filter)
