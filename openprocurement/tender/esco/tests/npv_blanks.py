import datetime

from openprocurement.tender.esco.utils import calculate_npv
from openprocurement.tender.esco.npv_calculation import (
    calculate_contract_duration,
    calculate_days_with_cost_reduction,
    calculate_days_for_discount_rate
)
from openprocurement.tender.esco.constants import DAYS_PER_YEAR, NPV_CALCULATION_DURATION

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
        [347, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365]
    )
    
    announcement_date = datetime.date(2019, 1, 20)
    self.assertEqual(
        calculate_days_with_cost_reduction(DAYS_PER_YEAR, announcement_date),
        [346, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365, 365]
    )


def days_for_discount_rate(self):
    announcement_date = datetime.date(2017, 8, 18)
    days = calculate_days_for_discount_rate(DAYS_PER_YEAR, announcement_date)
    # (NPV_CALCULATION_DURATION - 1) is a number of full years
    expected_days = [135] + [365] * (NPV_CALCULATION_DURATION - 1) + [230]
    self.assertEqual(days, expected_days)

    anouncement_date = datetime.date(2020, 1, 20)
    days = calculate_days_for_discount_rate(DAYS_PER_YEAR, announcement_date)
    expected_days = [347] + [365] * (NPV_CALCULATION_DURATION - 1) + [19]
    self.assertEqual(days, expected_dayes)

    anouncement_date = datetime.date(2019, 1, 20)
    days = calculate_days_for_discount_rate(DAYS_PER_YEAR, announcement_date)
    expected_days = [346] + [365] * (NPV_CALCULATION_DURATION - 1) + [19]
    self.assertEqual(days, expected_dayes)


