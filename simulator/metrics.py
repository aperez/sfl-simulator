from .spectrum import *
from .spectrum_filter import *

def iterate_spectrum(spectrum, spectrum_filter=None, column_order=False):
    if not spectrum_filter:
        spectrum_filter = SpectrumFilter(spectrum)

    if column_order:
        for i_c, c in enumerate(spectrum_filter.components_filter):
            for i_t, t in enumerate(spectrum_filter.transactions_filter):
                activity = spectrum.get_activity(t, c)
                yield i_t, i_c, activity
    else:
        for i_t, t in enumerate(spectrum_filter.transactions_filter):
            for i_c, c in enumerate(spectrum_filter.components_filter):
                activity = spectrum.get_activity(t, c)
                yield i_t, i_c, activity


def metric(f):
    def wrapper(spectrum, spectrum_filter=None):
        components = spectrum.components
        transactions = spectrum.transactions
        if spectrum_filter:
            components = len(spectrum_filter.components_filter)
            transactions = len(spectrum_filter.transactions_filter)

        return f(spectrum, spectrum_filter, components, transactions)
    return wrapper

@metric
def coverage(spectrum, spectrum_filter, components, transactions):
    component_coverage = [0] * components
    for _, c, activity in iterate_spectrum(spectrum, spectrum_filter):
        component_coverage[c] |= activity
    return sum(component_coverage) / components

@metric
def density(spectrum, spectrum_filter, components, transactions):
    activations = 0
    for _, _, activity in iterate_spectrum(spectrum, spectrum_filter):
        activations += activity
    return activations / (components * transactions)

@metric
def diversity(spectrum, spectrum_filter, components, transactions):
    transaction_coverages = {}
    current_transaction = -1
    current_coverage = None

    for t, c, activity in iterate_spectrum(spectrum, spectrum_filter):
        if current_transaction != t:
            if current_coverage:
                str_coverage = str(current_coverage)
                value = transaction_coverages.get(str_coverage, 0)
                transaction_coverages[str_coverage] = value + 1

            current_transaction = t
            current_coverage = []

        if activity != 0:
            current_coverage.append(c)

    if current_coverage:
        str_coverage = str(current_coverage)
        value = transaction_coverages.get(str_coverage, 0)
        transaction_coverages[str_coverage] = value + 1

    num, denum = 0.0, 0.0
    for value in transaction_coverages.values():
        num += (value * (value - 1))
        denum += value

    div = 0.0 if denum - 1 <= 0 else 1.0 - num / (denum * (denum - 1))
    return div

@metric
def uniqueness(spectrum, spectrum_filter, components, transactions):
    component_coverages = set()
    current_component = -1
    current_coverage = None

    for t, c, activity in iterate_spectrum(spectrum, spectrum_filter, True):
        if current_component != c:
            if current_coverage:
                component_coverages.add(str(current_coverage))
            current_component = c
            current_coverage = []

        if activity != 0:
            current_coverage.append(t)

    if current_coverage:
        component_coverages.add(str(current_coverage))

    return len(component_coverages) / components

def ddu(spectrum, spectrum_filter = None):
    density_value = density(spectrum, spectrum_filter)
    diversity_value = diversity(spectrum, spectrum_filter)
    uniqueness_value = uniqueness(spectrum, spectrum_filter)
    ddu_value = (1.0 - abs(1.0 - 2.0 * density_value)) *\
                diversity_value *\
                uniqueness_value
    return ddu_value, density_value, diversity_value, uniqueness_value
