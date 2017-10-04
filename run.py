import simulator

if __name__ == "__main__":
    generator = simulator.TopologyGenerator(20)
    topology = generator.generate()
    #topology.print_plot()

    activator = simulator.CoverageActivator(topology)
    simulated_transactions = activator.generate()

    for s in simulated_transactions.sample_spectra(3):
        f = s.inject_faults(num_faults=1)
        print("\nSpectrum:")
        s.print_spectrum()

        mhs = simulator.MHS()
        trie = mhs.calculate(s)
        for candidate in trie:
            print(candidate)
