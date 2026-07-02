from .empty import empty_modifier

def gender_modifier(form_a):
    result = empty_modifier()

    if form_a.gender == "1":

        result["obgyn"]["modifier"] = -100
        result["obgyn"]["reasons"].append("رشته زنان برای آقایان پیشنهاد نمی‌شود.")
        result["obgyn"]["red_flags"].append("red_flags")

    else:

        result["general_surgery"]["modifier"] -= 1
        result["urology"]["modifier"] -= 2
        result["neurosurgery"]["modifier"] -= 3

    return result
