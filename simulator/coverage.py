import simulator.spectrum
import random

class CoverageActivator(object):
    def __init__(self, topology):
        self.taxonomy = topology.taxon_namespace
        self.components = len(self.taxonomy)
        self.pdm = topology.phylogenetic_distance_matrix()

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

    def propagate(self, base, active_component, coef):
        transaction = base[:]

        for c in range(self.components):
            if c == active_component:
                transaction[c] = 1
            else:
                distance = self.pdm.distance(self.taxonomy[c],
                                             self.taxonomy[active_component],
                                             is_weighted_edge_distances=False)
                p = (self.components - distance) / self.components
                transaction[c] |= 1 if coef * random.random() >= p else 0
        return transaction
