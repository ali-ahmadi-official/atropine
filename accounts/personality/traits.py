from statistics import mean

def question_score(raw_score: int | str, reverse: bool = False) -> int:
    score = int(raw_score)
    return 6 - score if reverse else score

def calculate_item_scores(answers: dict) -> dict:
    items = {
        "patient_relation": ("گرایش به ارتباط مستقیم و مستمر با بیمار", [(1, False), (2, False), (3, False)]),
        "empathy": ("همدلی و درگیری عاطفی با وضعیت بیمار", [(4, False), (5, False), (6, True)]),
        "stress_tolerance": ("تاب‌آوری در شرایط بحرانی و استرس لحظه‌ای", [(7, False), (8, False), (9, True), (10, False)]),
        "burnout_tolerance": ("تحمل فشار کاری مزمن و فرسودگی", [(11, False), (12, True), (13, False)]),
        "physical_endurance": ("توان جسمی برای کار طولانی، ایستادن و کشیک", [(14, False), (15, True), (16, False)]),
        "manual_skill": ("گرایش به کارهای دستی، اجرایی و مهارت‌های عملی", [(17, False), (18, False), (19, False), (20, True)]),
        "precision": ("علاقه به ظرافت، دقت بالا و کارهای میکرو", [(21, False), (22, False), (23, True)]),
        "diagnostic_reasoning": ("علاقه به تحلیل و حل مسئله تشخیصی", [(24, False), (25, False), (26, False), (27, True)]),
        "ambiguity_tolerance": ("تحمل ابهام و قطعیت‌نداشتن", [(28, False), (29, False), (30, True)]),
        "rapid_result": ("تمایل به دیدن نتیجه سریع و ملموس", [(31, False), (32, False), (33, False)]),
        "long_term_followup": ("علاقه به پیگیری طولانی‌مدت بیمار", [(34, False), (35, False), (36, True)]),
        "teamwork": ("تمایل به کار تیمی در قالب تیم درمان", [(37, False), (38, False), (39, True)]),
        "independence": ("تمایل به استقلال در تصمیم‌گیری و شیوه کار", [(40, False), (41, False), (42, False)]),
        "work_life_balance": ("اهمیت تعادل بین کار و زندگی شخصی", [(43, False), (44, False), (45, False), (46, True)]),
        "academic_orientation": ("گرایش به مطالعه، آموزش و فعالیت علمی", [(47, False), (48, False), (49, True)]),
        "technology_interest": ("علاقه به ابزار، دستگاه و فناوری پزشکی", [(50, False), (51, False), (52, True)]),
        "pediatrics_flag": ("علاقه خاص به کار در حوزه کودکان و نوزادان", [(53, False), (54, False)]),
        "psychiatry_flag": ("علاقه خاص به حوزه سلامت روان", [(55, False), (56, False)]),
        "blood_trauma_flag": ("حساسیت/راحتی نسبت به خون، تروما و صحنه‌های شدید", [(57, False), (58, True)]),
        "surgical_mindset": ("ذهنیت مداخله‌گر و جراحی‌محور", [(59, False), (60, True)]),
    }

    result = {}

    for key, (name, questions) in items.items():
        scores = [
            question_score(answers[f"q{q}"], reverse)
            for q, reverse in questions
        ]

        result[key] = {
            "name": name,
            "score": round(mean(scores), 2),
        }

    return result