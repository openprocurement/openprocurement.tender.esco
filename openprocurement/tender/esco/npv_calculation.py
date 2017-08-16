from openprocurement.tender.esco.constants import DAYS_PER_YEAR, NPV_CALCULATION_DURATION
from fractions import Fraction
import datetime


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


ANNOUNCEMENT_DATE = datetime.date(2017, 8, 18)


def calculate_days_with_cost_reduction(
        days_per_year=DAYS_PER_YEAR,
        announcement_date=ANNOUNCEMENT_DATE):
    first_year_days = (datetime.date(announcement_date.year, 12, 31) - announcement_date).days
    return [first_year_days] + [days_per_year] * NPV_CALCULATION_DURATION


def calculate_days_for_discount_rate(
        days_per_year=DAYS_PER_YEAR,
        announcement_date=ANNOUNCEMENT_DATE):
    days = calculate_days_with_cost_reduction(days_per_year, announcement_date)[:-1]
    days.append(days_per_year - days[0])
    return days


def calculate_days_with_payments(
        contract_duration_years,
        contract_duration_days,
        announcement_date=ANNOUNCEMENT_DATE,
        days_per_year=DAYS_PER_YEAR):
    contract_duration = calculate_contract_duration(contract_duration_years, contract_duration_days, days_per_year)
    days = [min(contract_duration, calculate_days_with_cost_reduction(days_per_year, announcement_date)[0])]
    contract_duration -= days[0]
    days += [days_per_year] * (contract_duration // days_per_year) + [contract_duration % days_per_year]
    if len(days) < NPV_CALCULATION_DURATION + 1:
        days += [0] * (NPV_CALCULATION_DURATION + 1 - len(days))
    return days


def calculate_income(client_cost_reductions, client_payments):
	return map(lambda x, y: x - y, client_cost_reductions, client_payments)
