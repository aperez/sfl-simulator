import simulator.spectrum
import random

class CoverageActivator(object):
    def __init__(self, topology):
        self.taxonomy = topology.taxon_namespace
        self.components = len(self.taxonomy)
        self.pdm = topology.phylogenetic_distance_matrix()
        self.distances = {}

    def generate(self, seed=None, reps=10, coefs=[0.85, 1.00, 2.00, 3.00]):
        if seed is not None:
            random.seed(seed)

        spectrum = simulator.spectrum.Spectrum()
        base = [0] * (self.components + 1)

        for coef in coefs:
            for c in range(self.components):
                for _ in range(reps):
                    t = self.propagate(base, c, coef)
                    spectrum.append_transaction(t)

        spectrum.calculate_dimensions()
        return spectrum

    def get_distance(self, c1, c2):
        if (c1, c2) in self.distances:
            return self.distances[(c1, c2)]
        if (c2, c1) in self.distances:
            return self.distances[(c2, c1)]
        distance = self.pdm.distance(self.taxonomy[c1],
                                     self.taxonomy[c2],
                                     is_weighted_edge_distances=False)
        self.distances[(c1, c2)] = distance
        return distance

    def propagate(self, base, active_component, coef):
        transaction = base[:]

        for c in range(self.components):
            if c == active_component:
                transaction[c] = 1
            else:
                distance = self.get_distance(c, active_component)
                p = (self.components - distance) / self.components
                transaction[c] |= 1 if coef * random.random() >= p else 0
        return transaction
