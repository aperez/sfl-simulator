import simulator

if __name__ == "__main__":
    generator = simulator.TopologyGenerator(20)
    topology = generator.generate()
    #topology.print_plot()

    activator = simulator.CoverageActivator(topology)
    simulated_transactions = activator.generate()

    for s in simulated_transactions.sample_spectra(3):
        print("\nSpectrum:")
        s.print_spectrum()
