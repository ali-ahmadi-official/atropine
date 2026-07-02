from .empty import empty_modifier
from ..dicts import (
    SURGERY_MAJOR,
    SURGERY_MINOR,
    NON_SURGERY_MAJOR,
    NON_SURGERY_MINOR,
)


def internship_modifier(form):
    result = empty_modifier()

    group_map = {
        "1": SURGERY_MAJOR,
        "2": SURGERY_MINOR,
        "3": NON_SURGERY_MAJOR,
        "4": NON_SURGERY_MINOR,
    }

    for group in form.better_activity:
        if group in group_map:
            for specialty in group_map[group]:
                result[specialty]["modifier"] += 2

    for group in form.favorite_activity:
        if group in group_map:
            for specialty in group_map[group]:
                result[specialty]["modifier"] += 2

    if form.guard == "1":

        for specialty in (
            SURGERY_MAJOR
            + SURGERY_MINOR
            + NON_SURGERY_MAJOR
        ):
            result[specialty]["modifier"] += 1

    elif form.guard == "3":

        for specialty in SURGERY_MAJOR:
            result[specialty]["modifier"] -= 2

        for specialty in SURGERY_MINOR:
            result[specialty]["modifier"] -= 1

        for specialty in NON_SURGERY_MAJOR:
            result[specialty]["modifier"] -= 1

    for specialty in result:
        result[specialty]["modifier"] = max(
            -4,
            min(5, result[specialty]["modifier"])
        )

    return result