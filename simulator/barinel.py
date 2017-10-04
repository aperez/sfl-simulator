from .spectrum_filter import *

import operator


class Barinel(object):

    def __init__(self):
        self._lambda = 1
        self.epsilon = 0.0001
        self.pr = 0.001

    def diagnose(self,  spectrum, candidate_trie, spectrum_filter=None):
        self.spectrum = spectrum

        if not spectrum_filter:
            spectrum_filter = SpectrumFilter(self.spectrum)

        self.spectrum_filter = spectrum_filter

        total = 0
        tmp = []
        for candidate in candidate_trie:
            prob = self.candidate_probability(candidate)
            total += prob
            tmp.append((candidate, prob))

        report = []
        for candidate, prob in tmp:
            report.append((candidate, prob/total))

        return sorted(report, key=operator.itemgetter(1), reverse=True)

    def candidate_probability(self, candidate):

        self.goodness_model(candidate)
        goodnesses = [0.5 for _ in range(len(candidate))]

        prob = self.probability(candidate, goodnesses)

        while True:
            old_prob = prob

            goodnesses = self.update_goodnesses(goodnesses)
            prob = self.probability(candidate, goodnesses)

            if self.stop_condition(prob, old_prob):
                break

        prob *= self.prior(candidate)

        return prob

    def probability(self, candidate, goodnesses):

        prob = 1.0

        for t in self.spectrum_filter.transactions_filter:
            tmp = 1.0
            activity = self.spectrum.get_transaction_activity(t)

            for i, component in enumerate(candidate):
                if activity[component]:
                    tmp *= goodnesses[i]

            if activity[-1]:
                tmp = 1.0 - tmp

            prob *= tmp

        return prob

    def prior(self, candidate):
        candidate_size = len(candidate)
        return self.pr ** candidate_size

    def stop_condition(self, prob, old_prob):
        return 2 * (prob - old_prob) / abs(prob + old_prob) < self.epsilon

    def goodness_model(self, candidate):
        candidate_length = len(candidate)
        self.passes = [0 for _ in range(1 << candidate_length)]
        self.fails = [0 for _ in range(1 << candidate_length)]

        for t in self.spectrum_filter.transactions_filter:
            pattern = 0
            activity = self.spectrum.get_transaction_activity(t)

            for i, component in enumerate(candidate):
                if activity[component]:
                    pattern += 1 << i

            if pattern:
                if activity[-1]:
                    self.fails[pattern] += 1
                else:
                    self.passes[pattern] += 1

    def update_goodnesses(self, goodnesses):
        gradient = self.gradient(goodnesses)
        return self.update(goodnesses, gradient)

    def gradient(self, goodnesses):
        candidate_size = len(goodnesses)
        gradient = [0.0 for _ in range(candidate_size)]

        for pattern in range(1 << candidate_size):
            passes = self.passes[pattern]
            fails = self.fails[pattern]

            if not fails and not passes:
                continue

            tmp = 1.0

            for c in range(candidate_size):
                gradient[c] += passes / goodnesses[c]
                if pattern & 1 << c:
                    tmp *= goodnesses[c]

            for c in range(candidate_size):
                if pattern & 1 << c:
                    gradient[c] += -fails * (tmp / goodnesses[c]) * (1.0 - tmp)

        return gradient

    def update(self, goodnesses, gradient):
        new_goodnesses = goodnesses[:]

        for c, goodness in enumerate(goodnesses):
            if gradient[c] == 0:
                continue

            new_goodnesses[c] = goodness + \
                (self._lambda * goodness / gradient[c])

            if new_goodnesses[c] <= 0:
                new_goodnesses[c] = self.epsilon
            elif new_goodnesses[c] > 1:
                new_goodnesses[c] = 1

        return new_goodnesses
