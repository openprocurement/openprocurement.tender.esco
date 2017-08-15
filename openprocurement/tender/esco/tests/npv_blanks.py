import datetime

from openprocurement.tender.esco.utils import calculate_npv
from openprocurement.tender.esco.npv_calculation import (
    calculate_contract_duration,
    calculate_days_with_cost_reduction,
    calculate_days_for_discount_rate
)
from openprocurement.tender.esco.constants import DAYS_PER_YEAR

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


def days_for_discount_rate(self):
    days_per_year = 365
    announcement_date = datetime.date(2017, 8, 18)
    npv_calculation_declaration = 20

    days = calculate_days_for_discount_rate(days_per_year, announcement_date)
    expected_days = [135] + [365] * 19 + [230]
    self.assertEqual(days, expected_days)

