from .ranker import *
from .spectrum import *
from .spectrum_filter import *
from .trie import *

class MHS(object):
    def __init__(self, l=8):
        self.ranker = SimilarityRanker(ochiai)
        self.cutoff = l
        self.epsilon = 0.0001

    def calculate(self, spectrum, spectrum_filter=None):
        self.spectrum = spectrum

        if not spectrum_filter:
            spectrum_filter = SpectrumFilter(self.spectrum)

        spectrum_filter.filter_passing_transactions(self.spectrum)
        self.candidates = Trie()
        self.calculate_mhs(spectrum_filter, [])
        return self.candidates

    def calculate_mhs(self, spectrum_filter, d):
        if spectrum_filter.has_failing_transactions(self.spectrum):
            if len(d) + 1 >= self.cutoff:
                return

            r = self.ranker.rank(self.spectrum, spectrum_filter=spectrum_filter)

            removed_components = 0
            for component, coefficient in reversed(r):
                if coefficient < self.epsilon:
                    spectrum_filter.filter_component(component)
                    removed_components += 1
                else:
                    break

            if removed_components:
                r = r[:-removed_components]

            for component, coefficient in r:
                new_spectrum_filter = spectrum_filter.copy()
                new_spectrum_filter.strip_component(self.spectrum, component)
                spectrum_filter.filter_component(component)
                self.calculate_mhs(new_spectrum_filter, d + [component])

        elif d:
            self.candidates.add_candidate(sorted(d))
