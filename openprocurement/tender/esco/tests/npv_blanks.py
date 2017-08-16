from openprocurement.tender.esco.utils import calculate_npv
from openprocurement.tender.esco.constants import DAYS_PER_YEAR, NPV_CALCULATION_DURATION
from openprocurement.tender.esco.npv_calculation import (
    calculate_contract_duration,
    calculate_discount_rate,
    calculate_discount_rates,
    calculate_days_with_cost_reduction,
    calculate_days_for_discount_rate,
    calculate_days_with_payments,
    calculate_income,
)
import datetime
from fractions import Fraction

nbu_rate = 0.22


def contract_duration(self):
    # Minimal contract duration
    years = 0
    days = 1
    self.assertEqual(
        calculate_contract_duration(years, days),
        years * DAYS_PER_YEAR + days,
    )

    years = 0
    days = 364
    self.assertEqual(
        calculate_contract_duration(years, days),
        years * DAYS_PER_YEAR + days,
    )

    years = 5
    days = 275
    self.assertEqual(
        calculate_contract_duration(years, days),
        years * DAYS_PER_YEAR + days,
    )

    # Max contract duration
    years = 15
    days = 0
    self.assertEqual(
        calculate_contract_duration(years, days),
        years * DAYS_PER_YEAR + days,
    )



def days_with_cost_reduction(self):
    # First test
    announcement_date = datetime.date(2017, 8, 18)
    self.assertEqual(
        calculate_days_with_cost_reduction(DAYS_PER_YEAR, announcement_date),
        [135, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365]
    )
    
    announcement_date = datetime.date(2020, 1, 20)
    self.assertEqual(
        calculate_days_with_cost_reduction(DAYS_PER_YEAR, announcement_date),
        [346, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365]
    )
    
    announcement_date = datetime.date(2019, 1, 20)
    self.assertEqual(
        calculate_days_with_cost_reduction(DAYS_PER_YEAR, announcement_date),
        [345, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365]
    )


def days_for_discount_rate(self):
    announcement_date = datetime.date(2017, 8, 18)
    days = calculate_days_for_discount_rate(DAYS_PER_YEAR, announcement_date)
    # (NPV_CALCULATION_DURATION - 1) is a number of full years
    expected_days = [135] + [365] * (NPV_CALCULATION_DURATION - 1) + [230]
    self.assertEqual(days, expected_days)

    announcement_date = datetime.date(2020, 1, 20)
    days = calculate_days_for_discount_rate(DAYS_PER_YEAR, announcement_date)
    expected_days = [346] + [365] * (NPV_CALCULATION_DURATION - 1) + [19]
    self.assertEqual(days, expected_days)

    announcement_date = datetime.date(2019, 1, 20)
    days = calculate_days_for_discount_rate(DAYS_PER_YEAR, announcement_date)
    expected_days = [345] + [365] * (NPV_CALCULATION_DURATION - 1) + [20]
    self.assertEqual(days, expected_days)


def discount_rate(self):

    # Predefined value
    nbu_rate = 12.5
    days = 135
    self.assertEqual(
        calculate_discount_rate(days, nbu_rate),
        4.623287671232877,
    )

    # Divide 100% by n parts and check if nbu_rate is the same as
    # nbu_rate * DAYS_PER_YEAR / DAYS_PER_YEAR
    n = 97
    for i in range(n + 1):
        nbu_rate = (i / float(n)) * 100
        days = DAYS_PER_YEAR
        self.assertEqual(
            calculate_discount_rate(days, nbu_rate, DAYS_PER_YEAR),
            nbu_rate,
        )


def discount_rates(self):

    periods = 21

    # All days for discount rate are zeros
    empty = [0] * periods
    empty_rates = calculate_discount_rates(empty, nbu_rate)
    self.assertEqual(len(empty), len(empty_rates))
    for rate in empty_rates:
        self.assertEqual(rate, 0)

    # All days for discount rate are equal to DAYS_PER_YEAR
    days = [DAYS_PER_YEAR] * periods
    calculated_rates = calculate_discount_rates(days, nbu_rate)
    self.assertEqual(len(days), len(calculated_rates))
    for rate in calculated_rates:
        self.assertEqual(rate, nbu_rate)

    # All days for discount rate are DIFFERENT
    # This code checks if calculated rates are also DIFFERENT
    days_increment = int(DAYS_PER_YEAR / periods)
    days = [(i + 1) * days_increment for i in range(21)]
    calculated_rates = calculate_discount_rates(days, nbu_rate)
    for (i, rate) in enumerate(calculated_rates):
        checking_rates = calculated_rates[i + 1:]
        for checking_rate in checking_rates:
            self.assertNotEqual(rate, checking_rate)

    # Predefined first and last value
    new_nbu_rate = 12.5
    predefined_rate1 = 4.623287671232877
    predefined_rate2 = 7.876712328767123

    days = [135] + [0] * (periods - 2) + [230]
    calculated_rates = calculate_discount_rates(days, new_nbu_rate)
    self.assertEqual(len(days), len(calculated_rates))
    self.assertEqual(calculated_rates[0], predefined_rate1)
    self.assertEqual(calculated_rates[-1], predefined_rate2)


def days_with_payments(self):
    days = calculate_days_with_payments(3, 0)
    expected_days = [135, 365, 365, 230] + [0] * 17
    self.assertEqual(days, expected_days)


def income(self):
    client_cost_reductions = [Fraction("92.47")] + [Fraction("250.0")] * 20
    client_payments = [Fraction("64.73"), Fraction("175.0"), Fraction("175.0"), Fraction("110.27")] +\
    [Fraction("0.0")] * 17
    client_income = calculate_income(client_cost_reductions, client_payments)
    expected_client_income = [Fraction("27.74"), Fraction("75.0"), Fraction("75.0"), Fraction("139.73")] +\
    [Fraction("250.0")] * 17
    self.assertEqual(client_income, expected_client_income)
