from .empty import empty_modifier
from ..dicts import (
    SURGERY_MAJOR,
    SURGERY_MINOR,
    NON_SURGERY_MAJOR,
    NON_SURGERY_MINOR,
)

def career_modifier(form):
    result = empty_modifier()

    if form.interest_surgical == "3":
        for s in SURGERY_MAJOR + SURGERY_MINOR:
            result[s]["modifier"] += 2

    elif form.interest_surgical == "1":
        for s in SURGERY_MAJOR:
            result[s]["modifier"] -= 3

        for s in SURGERY_MINOR:
            result[s]["modifier"] -= 2

    if form.interest_non_surgical == "3":
        for s in NON_SURGERY_MAJOR + NON_SURGERY_MINOR:
            result[s]["modifier"] += 2

    elif form.interest_non_surgical == "1":
        for s in NON_SURGERY_MAJOR:
            result[s]["modifier"] -= 3

        for s in NON_SURGERY_MINOR:
            result[s]["modifier"] -= 2

    if form.interest_non_surgical != "1":

        if form.field_preference == "1":

            result["internal_medicine"]["modifier"] += 1
            result["cardiology"]["modifier"] += 1
            result["neurology"]["modifier"] += 1
            result["psychiatry"]["modifier"] += 1
            result["occupational_medicine"]["modifier"] += 1

            result["radiology"]["modifier"] -= 1
            result["pathology"]["modifier"] -= 1
            result["nuclear_medicine"]["modifier"] -= 1
            result["radiation_oncology"]["modifier"] -= 1

        elif form.field_preference == "2":

            result["cardiology"]["modifier"] += 1
            result["dermatology"]["modifier"] += 1
            result["physical_medicine"]["modifier"] += 1
            result["radiology"]["modifier"] += 1

    if form.paraclinic_preference == "3":

        result["radiology"]["modifier"] += 2
        result["pathology"]["modifier"] += 2
        result["nuclear_medicine"]["modifier"] += 2
        result["radiation_oncology"]["modifier"] += 2

    elif form.paraclinic_preference == "1":

        result["radiology"]["modifier"] -= 2
        result["pathology"]["modifier"] -= 3
        result["nuclear_medicine"]["modifier"] -= 2
        result["radiation_oncology"]["modifier"] -= 2

    return result