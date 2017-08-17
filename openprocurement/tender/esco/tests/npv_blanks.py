from datetime import date
from openprocurement.tender.esco.tests.npv_test_data import DISCOUNT_COEF, DISKOUNT_RATE
from openprocurement.tender.esco.constants import DAYS_PER_YEAR, NPV_CALCULATION_DURATION
from openprocurement.tender.esco.npv_calculation import (
    calculate_contract_duration,
    calculate_discount_rate,
    calculate_discount_rates,
    calculate_discount_coef,
    calculate_days_with_cost_reduction,
)

nbu_rate = 0.22


def discount_coef(self):
    discount_rate = DISKOUNT_RATE['first_test']
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        DISCOUNT_COEF['first_test']
    )

    discount_rate = DISKOUNT_RATE['second_test']
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        DISCOUNT_COEF['second_test']
    )

    discount_rate = DISKOUNT_RATE['third_test']
    self.assertEqual(
        calculate_discount_coef(discount_rate),
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


def days_with_cost_reduction(self):
    # First test
    announcement_date = date(2017, 8, 18)
    self.assertEqual(
        calculate_days_with_cost_reduction(announcement_date, DAYS_PER_YEAR),
        [135] + [365] * NPV_CALCULATION_DURATION
    )

    announcement_date = date(2020, 01, 20)
    self.assertEqual(
        calculate_days_with_cost_reduction(announcement_date, DAYS_PER_YEAR),
        [346] + [365] * NPV_CALCULATION_DURATION
    )

    announcement_date = date(2019, 01, 20)
    self.assertEqual(
        calculate_days_with_cost_reduction(announcement_date, DAYS_PER_YEAR),
        [345] + [365] * NPV_CALCULATION_DURATION
    )
