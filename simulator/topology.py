import dendropy.simulate as treesim

class TopologyGenerator(object):
    def __init__(self, components=10):
        self.components = components
        self.default_args = {'birth_rate': 1.0, 'death_rate': 0.5}

    def generate(self, **kwargs):
        for key,value in self.default_args.items():
            if key not in kwargs:
                kwargs[key] = value
        kwargs['num_extant_tips'] = self.components

        return treesim.birth_death_tree(**kwargs)
