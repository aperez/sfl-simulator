import simulator
import argparse
import yaml

def generate_matrices(sim_settings, transactions):
    for remove_range in sim_settings["remove_ranges"]:
        for spectrum in transactions.sample_spectra(sim_settings["matrix_samples"]):

            working_spectrum = spectrum.copy()
            working_spectrum.remove_components(remove_range)

            for fault_pattern in sim_settings["injector"]["fault_patterns"]:
                for goodness in sim_settings["injector"]["goodnesses"]:
                    faulty_spectrum = working_spectrum.copy()
                    for cardinality in fault_pattern:
                        faulty_spectrum.inject_fault(cardinality=cardinality)
                    yield faulty_spectrum

def simulate(settings):
    sim_settings = settings["simulation"]

    barinel = simulator.BarinelNative()
    matrix_id = 0

    with simulator.Reporter(settings["output"]["report"]) as reporter:
        for components in sim_settings["components"]:
            generator = simulator.TopologyGenerator(components)
            topology = generator.generate()
            activator = simulator.CoverageActivator(topology)

            reps = sim_settings["activator"]["reps"]
            for coefs in sim_settings["activator"]["coefs"]:
                simulated_transactions = activator.generate(reps=reps, coefs=coefs)

                for spectrum in generate_matrices(sim_settings, simulated_transactions):
                    spectrum.id = matrix_id
                    matrix_id += 1

                    report = barinel.diagnose(spectrum)
                    reporter.write(spectrum, report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="SFL Simulator")
    parser.add_argument("--sim", help="Simulate", action="store_true")
    parser.add_argument("--plot", help="Plot results", action="store_true")
    args = parser.parse_args()

    with open("experiment.yml") as e:
        experiment_settings = yaml.load(e)

        if args.sim:
            simulate(experiment_settings)
        if args.plot:
            simulator.plot_report(experiment_settings)
