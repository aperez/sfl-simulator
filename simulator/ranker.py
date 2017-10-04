from .spectrum_filter import SpectrumFilter

import math
import operator

def ochiai(n):
    res = math.sqrt(n[1][1] + n[0][1]) * math.sqrt(n[1][1] + n[1][0])
    if res == 0.0:
        return 0.0
    else:
        return n[1][1] / res

class SimilarityRanker(object):

    def __init__(self, heuristic=ochiai):
        self.heuristic = heuristic

    def rank(self, spectrum, spectrum_filter=None):
        if not spectrum_filter:
            spectrum_filter = SpectrumFilter(spectrum)

        ranking = []
        error = {}
        for t in spectrum_filter.transactions_filter:
            error[t] = spectrum.is_error(t)

        for c in spectrum_filter.components_filter:
            n = [[0, 0], [0, 0]]

            for t in spectrum_filter.transactions_filter:
                activity = spectrum.get_activity(t, c)
                n[1 if activity else 0][1 if error[t] else 0] += 1

            ranking.append((c, self.heuristic(n)))

        return sorted(ranking, key=operator.itemgetter(1), reverse=True)
