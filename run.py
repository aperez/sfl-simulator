import simulator

if __name__ == "__main__":
    generator = simulator.TopologyGenerator(20)
    topology = generator.generate()
    #topology.print_plot()

    activator = simulator.CoverageActivator(topology)
    simulated_transactions = activator.generate()

    mhs = simulator.MHS()
    barinel = simulator.Barinel()

    with simulator.Reporter("output/report.csv") as reporter:
        matrix_id = 0
        for spectrum in simulated_transactions.sample_spectra(3):
            f = spectrum.inject_faults(num_faults=2)
            spectrum.id = matrix_id
            matrix_id += 1
            print("\nSpectrum:")
            spectrum.print_spectrum()

            trie = mhs.calculate(spectrum)
            report = barinel.diagnose(spectrum, trie)
            print(report)

            reporter.write(spectrum, report)
