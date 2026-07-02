from .empty import empty_modifier
from ..dicts import SPECIALTY_GROUPS

def calculate_family_load(form_a):
    score = 0

    if form_a.marital == "2":
        score += 1

        if form_a.wife_condition == "1":
            score += 2

        elif form_a.wife_condition in ["2", "3"]:
            score += 1

        if form_a.child == "2":
            score += 3

        elif form_a.child == "1":
            score += 1

    if form_a.family_support == "2":
        score += 1

    elif form_a.family_support == "1":
        score += 2

    return score

def family_modifier(form_a):
    result = empty_modifier()

    load = calculate_family_load(form_a)

    if load <= 1:

        return result

    elif load <= 3:

        major_surgery = -1
        minor_surgery = 0
        major_non = 0
        minor_non = 1

    elif load <= 5:

        major_surgery = -2
        minor_surgery = -1
        major_non = -1
        minor_non = 1

    else:

        major_surgery = -3
        minor_surgery = -2
        major_non = -2
        minor_non = 2

    for key in SPECIALTY_GROUPS["major_surgery"]:
        result[key]["modifier"] += major_surgery

    for key in SPECIALTY_GROUPS["minor_surgery"]:
        result[key]["modifier"] += minor_surgery

    for key in SPECIALTY_GROUPS["major_non_surgery"]:
        result[key]["modifier"] += major_non

    for key in SPECIALTY_GROUPS["minor_non_surgery"]:
        result[key]["modifier"] += minor_non

    return result
