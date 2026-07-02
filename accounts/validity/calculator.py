class AdmissionPredictor:

    def __init__(self, validity, university, field, underutilized):

        self.validity = validity

        self.university = {
            i["دانشگاه"]: i
            for i in university
        }

        self.field = {
            i["رشته"]: i
            for i in field
        }

        self.under = {
            i["رشته"]: i
            for i in underutilized
        }

    ########################################################

    def get_rank(self, rank):

        if rank.quota_25_rank:
            return "سهمیه 25%", rank.quota_25_rank

        if rank.quota_5_rank:
            return "سهمیه 5%", rank.quota_5_rank

        if rank.quota_city_1_rank:
            return "محروم", rank.quota_city_1_rank

        if rank.quota_city_2_rank:
            return "محروم", rank.quota_city_2_rank

        return "آزاد", rank.free_rank

    ########################################################

    def adjust_rank(self, last_rank, field, university, under):

        factor = 1

        # رشته (70%)
        if field and field["ظرفیت_کل_دوره_51"]:

            ratio = (
                field["ظرفیت_کل_دوره_52"] /
                field["ظرفیت_کل_دوره_51"]
            )

            factor += (ratio - 1) * 0.7

        # دانشگاه (20%)
        if university and university["ظرفیت_کل_دوره_51"]:

            ratio = (
                university["ظرفیت_کل_دوره_52"] /
                university["ظرفیت_کل_دوره_51"]
            )

            factor += (ratio - 1) * 0.2

        # محروم (10%)
        if under and under["ظرفیت_محروم_51"]:

            ratio = (
                under["ظرفیت_محروم_52"] /
                under["ظرفیت_محروم_51"]
            )

            factor += (ratio - 1) * 0.1

        return int(last_rank * factor)

    ########################################################

    def confidence(self, adjusted_rank, user_rank):

        if user_rank >= adjusted_rank:
            return 0

        return round(
            ((adjusted_rank - user_rank) / adjusted_rank) * 100,
            1
        )

    ########################################################

    def probability(self, confidence):

        if confidence >= 90:
            return "قطعی"

        if confidence >= 75:
            return "زیاد"

        if confidence >= 50:
            return "متوسط"

        if confidence >= 25:
            return "کم"

        return "بعید"

    ########################################################

    def predict(self, rank):

        quota, user_rank = self.get_rank(rank)

        result = []

        for item in self.validity:

            if item["سهمیه"] != quota:
                continue

            field = self.field.get(item["رشته قبولی"])

            university = self.university.get(item["دانشگاه"])

            under = None

            if quota == "محروم":
                under = self.under.get(item["رشته قبولی"])

            adjusted_rank = self.adjust_rank(
                item["رتبه"],
                field,
                university,
                under
            )

            conf = self.confidence(
                adjusted_rank,
                user_rank
            )

            result.append({

                "دانشگاه": item["دانشگاه"],

                "رشته": item["رشته قبولی"],

                "احتمال": self.probability(conf),

                "اعتماد": conf,

                "رتبه قبولی سال قبل": item["رتبه"],

                "رتبه تعدیل شده": adjusted_rank,

                "اختلاف رتبه": adjusted_rank-user_rank
            })

        result.sort(
            key=lambda x: (
                x["اعتماد"],
                x["رتبه تعدیل شده"]
            ),
            reverse=True
        )

        grouped = {
            "قطعی": [],
            "زیاد": [],
            "متوسط": [],
            "کم": [],
            "بعید": [],
        }

        for item in result:
            grouped[item["احتمال"]].append(item)

        return {
            key: value[:10]
            for key, value in grouped.items()
        }
