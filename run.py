import simulator
import argparse

def simulate(report_path):
    generator = simulator.TopologyGenerator(20)
    topology = generator.generate()
    #topology.print_plot()

    activator = simulator.CoverageActivator(topology)
    simulated_transactions = activator.generate()

    mhs = simulator.MHS()
    barinel = simulator.Barinel()

    with simulator.Reporter(report_path) as reporter:
        matrix_id = 0
        for spectrum in simulated_transactions.sample_spectra(3):
            f = spectrum.inject_fault(cardinality=1)
            spectrum.id = matrix_id
            matrix_id += 1
            print("\nSpectrum:")
            spectrum.print_spectrum()

            trie = mhs.calculate(spectrum)
            report = barinel.diagnose(spectrum, trie)
            print(report)

            reporter.write(spectrum, report)
            print(simulator.effort(spectrum, report))
            print(simulator.effort_reduced(spectrum, report))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="SFL Simulator")
    parser.add_argument("--sim", help="Simulate", action="store_true")
    parser.add_argument("--plot", help="Plot results", action="store_true")
    args = parser.parse_args()

    report_path = "output/report.csv"

    if args.sim:
        simulate(report_path)
    if args.plot:
        simulator.plot_report(report_path)
