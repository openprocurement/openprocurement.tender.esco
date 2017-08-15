announcement_date = "2017-08-18"
DAYS_IN_YEAR = 365


def calculate_days_for_discount_rate(announcement_date):
    days = calculate_days_with_cost_reduction(announcement_date)[:-1]
    days.append(DAYS_IN_YEAR - days[0])
    return days
