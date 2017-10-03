

class CoverageActivator(object):
    def __init__(self):
        pass

    def generate(self, topology):
        taxonomy = topology.taxon_namespace
        components = len(taxonomy)
        print("components:", components)
