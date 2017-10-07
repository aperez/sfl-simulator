import operator

def effort(spectrum, report):
    set_faults = [set(x) for x in spectrum.faults]
    lookup = [False] * len(spectrum.faults)

    gt_counter = 0
    eq_counter = 0
    current_value = None

    for entry, value in report:

        if current_value != value:
            #break if solution was found
            if len([x for x in lookup if not x]) == 0:
                break

            current_value = value
            gt_counter += eq_counter
            eq_counter = 1
        else:
            eq_counter += 1

        set_entry = set(entry)

        for i, fault in enumerate(set_faults):
            lookup[i] |= len(set_entry.intersection(fault)) > 0

    if eq_counter > 1:
        gt_counter += (eq_counter - 1) / 2.0

    return gt_counter

def effort_reduced(spectrum, report):
    set_faults = [set(x) for x in spectrum.faults]
    lookup = [False] * len(spectrum.faults)

    component_scores = {c: 0.0 for c in range(spectrum.components)}

    for entry, value in report:
        for c in entry:
            component_scores[c] += value

    component_scores = sorted(component_scores.items(),
                              key=operator.itemgetter(1),
                              reverse=True)

    gt_counter = 0
    eq_counter = 0
    current_value = None

    for c, value in component_scores:
        if current_value != value:
            #break if solution was found
            if len([x for x in lookup if not x]) == 0:
                break

            current_value = value
            gt_counter += eq_counter
            eq_counter = 1
        else:
            eq_counter += 1

        for i, fault in enumerate(set_faults):
            lookup[i] |= c in fault

    if eq_counter > 1:
        gt_counter += (eq_counter - 1) / 2.0

    return gt_counter
