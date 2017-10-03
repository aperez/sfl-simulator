import simulator

if __name__ == "__main__":
    generator = simulator.TopologyGenerator()
    topology = generator.generate()
    topology.print_plot()

    activator = simulator.CoverageActivator(topology)
    activator.generate()
