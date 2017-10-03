import simulator.spectrum

class CoverageActivator(object):
    def __init__(self, topology):
        self.taxonomy = topology.taxon_namespace
        self.components = len(self.taxonomy)
        self.pdm = topology.phylogenetic_distance_matrix()

    def generate(self):
        spectrum = simulator.spectrum.Spectrum()
        base = [0] * (self.components + 1)

        for c in range(self.components):
            t = self.propagate(base, c)
            spectrum.append_transaction(t)

        spectrum.calculate_dimensions()
        spectrum.print_spectrum()

    def propagate(self, base, active_component):
        transaction = base[:]

        for c in range(self.components):
            if c == active_component:
                transaction[c] = 1
            else:
                distance = self.pdm.distance(self.taxonomy[c],
                                             self.taxonomy[active_component],
                                             is_weighted_edge_distances=False)
        return transaction
