from datetime import date
from openprocurement.tender.esco.tests.npv_test_data import (
    DISCOUNT_COEF,
    DISCOUNT_RATE,
    DISCOUNTED_INCOME_COEF,
    INCOME_CUSTOMER,
    DISCOUNTED_INCOME_RES,
    COST_REDUCTIONS,
    PAYMENTS,
    EXPECTED_INCOME,
)
from openprocurement.tender.esco.constants import DAYS_PER_YEAR, NPV_CALCULATION_DURATION
from openprocurement.tender.esco.npv_calculation import (
    calculate_contract_duration,
    calculate_discount_rate,
    calculate_discount_rates,
    calculate_discounted_income,
    calculate_discount_coef,
    calculate_days_with_cost_reduction,
    calculate_days_for_discount_rate,
    calculate_days_with_payments,
    calculate_income,
)

nbu_rate = 0.22

def discount_coef(self):
    self.assertEqual(
        calculate_discount_coef(DISCOUNT_RATE['first_test']),
        DISCOUNT_COEF['first_test']
    )

    self.assertEqual(
        calculate_discount_coef(DISCOUNT_RATE['second_test']),
        DISCOUNT_COEF['second_test']
    )

    self.assertEqual(
        calculate_discount_coef(DISCOUNT_RATE['third_test']),
        DISCOUNT_COEF['third_test']
    )


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


def discounted_income(self):
    self.assertEqual(
        calculate_discounted_income(DISCOUNTED_INCOME_COEF['input_data'], INCOME_CUSTOMER['first_test']),
        DISCOUNTED_INCOME_RES['first_test']
    )

    self.assertEqual(
        calculate_discounted_income(DISCOUNTED_INCOME_COEF['input_data'], INCOME_CUSTOMER['second_test']),
        DISCOUNTED_INCOME_RES['second_test']
    )


def days_with_cost_reduction(self):
    announcement_date = date(2017, 8, 18)
    self.assertEqual(
        calculate_days_with_cost_reduction(announcement_date, DAYS_PER_YEAR),
        [135] + [365] * NPV_CALCULATION_DURATION
    )

    announcement_date = date(2020, 1, 20)
    self.assertEqual(
        calculate_days_with_cost_reduction(announcement_date, DAYS_PER_YEAR),
        [346] + [365] * NPV_CALCULATION_DURATION
    )

    announcement_date = date(2019, 1, 20)
    self.assertEqual(
        calculate_days_with_cost_reduction(announcement_date, DAYS_PER_YEAR),
        [345] + [365] * NPV_CALCULATION_DURATION
    )


def days_for_discount_rate(self):
    days = calculate_days_for_discount_rate([135] + [365] * NPV_CALCULATION_DURATION)
    # (NPV_CALCULATION_DURATION - 1) is a number of full years
    expected_days = [135] + [365] * (NPV_CALCULATION_DURATION - 1) + [230]
    self.assertEqual(days, expected_days)

    days = calculate_days_for_discount_rate([346] + [365] * NPV_CALCULATION_DURATION)
    expected_days = [346] + [365] * (NPV_CALCULATION_DURATION - 1) + [19]
    self.assertEqual(days, expected_days)

    days = calculate_days_for_discount_rate([345] + [365] * NPV_CALCULATION_DURATION)
    expected_days = [345] + [365] * (NPV_CALCULATION_DURATION - 1) + [20]
    self.assertEqual(days, expected_days)


def days_with_payments(self):
    days = calculate_days_with_payments(830, 135)
    expected_days = [135, 365, 330] + [0] * 18
    self.assertEqual(days, expected_days)


def income(self):
    client_cost_reductions = COST_REDUCTIONS['first_test']
    client_payments = PAYMENTS['first_test']
    client_income = calculate_income(client_cost_reductions, client_payments)
    expected_client_income = EXPECTED_INCOME['first_test']
    self.assertEqual(client_income, expected_client_income)
