from datetime import date
from fractions import Fraction
from openprocurement.tender.esco.constants import DAYS_PER_YEAR, NPV_CALCULATION_DURATION

DISCOUNT_RATE = [Fraction(str(4.623))]+[Fraction(str(12.500))]*19 + [Fraction(str(7.877))]


def calculate_discount_coef(discount_rate = DISCOUNT_RATE):
    discount_coef = []
    coefficient = Fraction(1)
    for i in discount_rate:
        coefficient = Fraction(coefficient, (Fraction(i, Fraction(100))+Fraction(1)))
        discount_coef.append(coefficient)
    return discount_coef

  
def calculate_contract_duration(
        contract_duration_years,
        contract_duration_days,
        days_per_year=DAYS_PER_YEAR):
    '''Calculate contract duration in days'''

    return contract_duration_years * days_per_year + contract_duration_days


def calculate_discount_rate(
        days_for_discount_rate,
        nbu_discount_rate,
        days_per_year=DAYS_PER_YEAR):
    '''Calculate discount rate according to the law'''

    return float(Fraction(nbu_discount_rate) *
                 Fraction(days_for_discount_rate, days_per_year))


def calculate_discount_rates(
        days_for_discount_rates,
        nbu_discount_rate,
        days_per_year=DAYS_PER_YEAR):
    '''Calculate discount rates from days_for_discount_rates list'''

    return [
        calculate_discount_rate(
            days_for_discount_rate,
            nbu_discount_rate,
            days_per_year,
        ) for days_for_discount_rate in days_for_discount_rates
    ]


def calculate_days_with_cost_reduction(
        announcement_date,
        days_per_year=DAYS_PER_YEAR,
        ):
    first_year_days = (date(announcement_date.year, 12, 31) - announcement_date).days
    return [first_year_days] + [days_per_year] * NPV_CALCULATION_DURATION
