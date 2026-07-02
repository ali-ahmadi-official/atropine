from ..dicts import SPECIALTIES

def empty_modifier():
    return {
        key: {
            "modifier": 0,
            "reasons": [],
            "red_flags": [],
        }
        for key in SPECIALTIES.keys()
    }
