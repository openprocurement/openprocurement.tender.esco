from datetime import date
from fractions import Fraction
from openprocurement.tender.esco.constants import DAYS_PER_YEAR, NPV_CALCULATION_DURATION


def calculate_discount_coef(discount_rate):
    discount_coef = []
    coefficient = Fraction(1)
    for i in discount_rate:
        coefficient = Fraction(coefficient, (i+Fraction(1)))
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


def calculate_discounted_income(coef_discount, income_customer):
    count = 0
    discounted_income = []
    for i in coef_discount:
        discounted_income.append(i*income_customer[count])
        count += 1
    return discounted_income

  
def calculate_days_with_cost_reduction(
        announcement_date,
        days_per_year=DAYS_PER_YEAR,
        ):
    first_year_days = (date(announcement_date.year, 12, 31) - announcement_date).days
    return [first_year_days] + [days_per_year] * NPV_CALCULATION_DURATION


def calculate_days_for_discount_rate(days_with_cost_reduction):
    days = days_with_cost_reduction[:-1]
    days.append(DAYS_PER_YEAR - days[0])
    return days


def calculate_days_with_payments(
        contract_duration,
        first_year_days,
        days_per_year=DAYS_PER_YEAR
        ):
    days = [min(contract_duration, first_year_days)]
    contract_duration -= days[0]
    days += [days_per_year] * (contract_duration // days_per_year) + [contract_duration % days_per_year]
    if (len(days) < NPV_CALCULATION_DURATION):
        days += [0] * (NPV_CALCULATION_DURATION + 1 - len(days))
    return days


def calculate_income(client_cost_reductions, client_payments):
    return [client_cost_reductions[i] - client_payments[i] for i in range(len(client_cost_reductions))]
