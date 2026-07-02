from .empty import empty_modifier


def level_from_10(value):
    value = int(value)

    if value <= 3:
        return "low"

    if value <= 7:
        return "medium"

    return "high"


def apply_modifier(modifier, table, factor=1):
    for specialty, value in table.items():
        modifier[specialty]["modifier"] += value * factor


def lifestyle_modifier(form):
    result = empty_modifier()

    level = level_from_10(form.income_importance)

    if level == "high":
        result["orthopedics"]["modifier"] += 2
        result["ophthalmology"]["modifier"] += 2
        result["ent"]["modifier"] += 2
        result["dermatology"]["modifier"] += 2
        result["radiology"]["modifier"] += 2

        result["urology"]["modifier"] += 1
        result["cardiology"]["modifier"] += 1
        result["general_surgery"]["modifier"] += 1
        result["neurosurgery"]["modifier"] += 1
        result["obgyn"]["modifier"] += 1
        result["physical_medicine"]["modifier"] += 1
        result["pathology"]["modifier"] += 1
        result["radiation_oncology"]["modifier"] += 1

    level = level_from_10(form.residency_free_time_importance)

    if level == "high":

        values = {
            "general_surgery": -3,
            "orthopedics": -3,
            "neurosurgery": -3,
            "ophthalmology": -1,
            "ent": -1,
            "urology": -1,
            "obgyn": -3,
            "internal_medicine": -2,
            "cardiology": -3,
            "neurology": -1,
            "dermatology": 3,
            "psychiatry": 3,
            "physical_medicine": 3,
            "sports_medicine": 3,
            "occupational_medicine": 3,
            "radiology": 2,
            "pathology": 2,
            "nuclear_medicine": 3,
            "radiation_oncology": 2,
        }

    elif level == "medium":

        values = {
            "general_surgery": -1.5,
            "orthopedics": -1.5,
            "neurosurgery": -1.5,
            "ophthalmology": -0.5,
            "ent": -0.5,
            "urology": -0.5,
            "obgyn": -1.5,
            "internal_medicine": -1,
            "cardiology": -1.5,
            "neurology": -0.5,
            "dermatology": 1.5,
            "psychiatry": 1.5,
            "physical_medicine": 1.5,
            "sports_medicine": 1.5,
            "occupational_medicine": 1.5,
            "radiology": 1,
            "pathology": 1,
            "nuclear_medicine": 1.5,
            "radiation_oncology": 1,
        }

    else:
        values = {}

    apply_modifier(result, values)

    level = level_from_10(form.career_free_time_importance)

    if level == "high":

        values = {
            "general_surgery": -3,
            "orthopedics": -2,
            "neurosurgery": -3,
            "ophthalmology": -2,
            "ent": -2,
            "urology": -1,
            "obgyn": -3,
            "internal_medicine": -2,
            "cardiology": -3,
            "neurology": -1,
            "dermatology": 3,
            "psychiatry": 3,
            "physical_medicine": 3,
            "sports_medicine": 3,
            "occupational_medicine": 3,
            "radiology": 3,
            "pathology": 3,
            "nuclear_medicine": 3,
            "radiation_oncology": 2,
        }

    elif level == "medium":

        values = {
            k: v / 2
            for k, v in {
                "general_surgery": -3,
                "orthopedics": -2,
                "neurosurgery": -3,
                "ophthalmology": -2,
                "ent": -2,
                "urology": -1,
                "obgyn": -3,
                "internal_medicine": -2,
                "cardiology": -3,
                "neurology": -1,
                "dermatology": 3,
                "psychiatry": 3,
                "physical_medicine": 3,
                "sports_medicine": 3,
                "occupational_medicine": 3,
                "radiology": 3,
                "pathology": 3,
                "nuclear_medicine": 3,
                "radiation_oncology": 2,
            }.items()
        }

    else:
        values = {}

    apply_modifier(result, values)

    level = level_from_10(form.no_night_shift_importance)

    if level == "high":

        values = {
            "general_surgery": -3,
            "orthopedics": -2,
            "neurosurgery": -3,
            "ophthalmology": -1,
            "ent": -1,
            "urology": -1,
            "obgyn": -3,
            "internal_medicine": -2,
            "cardiology": -3,
            "dermatology": 3,
            "psychiatry": 3,
            "physical_medicine": 3,
            "sports_medicine": 3,
            "occupational_medicine": 3,
            "radiology": 2,
            "pathology": 3,
            "nuclear_medicine": 3,
            "radiation_oncology": 3,
        }

    elif level == "medium":
        values = {k: v / 2 for k, v in values.items()}

    else:
        values = {}

    apply_modifier(result, values)

    if level_from_10(form.private_practice_interest) == "high":

        values = {
            "general_surgery": -1,
            "orthopedics": 1,
            "neurosurgery": -1,
            "ophthalmology": 2,
            "ent": 2,
            "urology": 1,
            "obgyn": 2,
            "internal_medicine": 2,
            "cardiology": 2,
            "neurology": 2,
            "dermatology": 2,
            "psychiatry": 2,
            "physical_medicine": 1,
            "sports_medicine": 1,
            "occupational_medicine": 2,
            "radiology": 1,
            "pathology": 1,
            "nuclear_medicine": -1,
            "radiation_oncology": 1,
        }

        apply_modifier(result, values)

    if level_from_10(form.academic_interest) == "high":

        for s in [
            "internal_medicine",
            "cardiology",
            "neurology",
            "pathology",
            "radiation_oncology",
        ]:
            result[s]["modifier"] += 1

    if level_from_10(form.immigration_interest) == "high":

        values = {
            "pathology": 2,
            "radiology": 1,
            "physical_medicine": 2,
            "neurology": 2,
            "internal_medicine": 1,
            "dermatology": 1,
            "nuclear_medicine": 1,
            "radiation_oncology": 1,
        }

        apply_modifier(result, values)

    return result