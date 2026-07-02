from .empty import empty_modifier
from .gender import gender_modifier
from .family import family_modifier
from .career import career_modifier
from .lifeftyle import lifestyle_modifier
from .internship import internship_modifier
from ..dicts import SPECIALTIES

def personal_modifier(form_a):
    gender = gender_modifier(form_a)
    family = family_modifier(form_a)
    career = career_modifier(form_a)
    lifestyle = lifestyle_modifier(form_a)
    internship = internship_modifier(form_a)

    result = empty_modifier()

    for specialty in SPECIALTIES.keys():

        total = (
            gender[specialty]["modifier"]
            + family[specialty]["modifier"]
            + career[specialty]["modifier"]
            + 0.8 * lifestyle[specialty]["modifier"]
            + internship[specialty]["modifier"]
        )

        total = max(-12, min(12, round(total, 2)))

        result[specialty]["modifier"] = total

        result[specialty]["reasons"] = (
            gender[specialty]["reasons"]
            + family[specialty]["reasons"]
            + career[specialty]["reasons"]
            + lifestyle[specialty]["reasons"]
            + internship[specialty]["reasons"]
        )

        result[specialty]["red_flags"] = (
            gender[specialty]["red_flags"]
            + family[specialty]["red_flags"]
            + career[specialty]["red_flags"]
            + lifestyle[specialty]["red_flags"]
            + internship[specialty]["red_flags"]
        )

    return result
