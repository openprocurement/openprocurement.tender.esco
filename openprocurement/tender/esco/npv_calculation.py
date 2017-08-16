from openprocurement.tender.esco.constants import DAYS_PER_YEAR
from fractions import Fraction


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


def calculate_amount_of_discounted_income(discounted_incomes):
    return sum(discounted_incomes)