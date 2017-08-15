import datetime
from constants import DAYS_PER_YEAR, ANNOUNCEMENT_DATE, 

def calculate_contract_duration(
        contract_duration_years,
        contract_duration_days,
        days_per_year=DAYS_PER_YEAR):
    '''Calculate contract duration in days'''

    return contract_duration_years * days_per_year + contract_duration_days


def calculate_days_with_cost_reduction(
        days_per_year=DAYS_PER_YEAR,
        announcement_date=ANNOUNCEMENT_DATE):
    
    first_year_days = (datetime.date(announcement_date.year, 12, 31) - announcement_date).days

    days = [first_year_days] + [days_per_year] * NPV_CALCULATION_DURATION
    return days


def calculate_days_for_discount_rate(
        days_per_year=DAYS_PER_YEAR,
        announcement_date=ANNOUNCEMENT_DATE):
    days = calculate_days_with_cost_reduction(days_per_year, announcement_date)[:-1]
    days.append(days_per_year - days[0])

    return days
