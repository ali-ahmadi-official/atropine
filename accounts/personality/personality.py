from .dicts import PERSONALITY_TYPES, SPECIALTIES, PERSONALITY_DETAILS

def detect_personality_type(item_scores):
    user_vector = [
        item["score"]
        for item in item_scores.values()
    ]

    best_key = None
    best_percent = -1

    for key, personality in PERSONALITY_TYPES.items():

        weights = personality["weights"]

        score = sum(
            value * weight
            for value, weight in zip(user_vector, weights)
        )

        max_score = 5 * sum(weights)

        percent = round(score / max_score * 100, 2)

        if percent > best_percent:
            best_percent = percent
            best_key = key

    details = PERSONALITY_DETAILS[best_key]

    return {
        "key": best_key,
        "percent": best_percent,
        **details
    }

def calculate_specialty_scores(item_scores):
    user_vector = [
        item["score"]
        for item in item_scores.values()
    ]

    results = []

    for key, specialty in SPECIALTIES.items():

        weights = specialty["weights"]

        score = sum(
            trait * weight
            for trait, weight in zip(user_vector, weights)
        )

        max_score = 5 * sum(weights)

        compatibility = round(score / max_score * 100, 2)

        results.append({
            "key": key,
            "name": specialty["name"],
            "score": score,
            "max_score": max_score,
            "percent": compatibility,
        })

    results.sort(
        key=lambda x: x["percent"],
        reverse=True,
    )

    return results

def apply_personal_modifier(specialty_results, personal_modifier):
    results = []

    for specialty in specialty_results:
        key = specialty["key"]

        adjusted_score = specialty["score"] + personal_modifier[key]["modifier"]

        # درصد جدید
        adjusted_percent = round(
            adjusted_score / specialty["max_score"] * 100,
            2
        )

        results.append({
            **specialty,
            "base_score": specialty["score"],
            "personal_modifier": personal_modifier[key]["modifier"],
            "adjusted_score": adjusted_score,
            "adjusted_percent": adjusted_percent,
            "reasons": personal_modifier[key]["reasons"],
            "red_flags": personal_modifier[key]["red_flags"],
        })

    results.sort(key=lambda x: x["adjusted_score"], reverse=True)

    return results

def categorize_specialties(results):
    recommended = []
    alternatives = []
    incompatible = []

    for item in results:

        if item["red_flags"]:
            incompatible.append(item)
            continue

        if item["adjusted_percent"] >= 80:
            recommended.append(item)

        elif item["adjusted_percent"] >= 60:
            alternatives.append(item)

        else:
            incompatible.append(item)

    return {
        "recommended": recommended,
        "alternatives": alternatives,
        "incompatible": incompatible,
    }
