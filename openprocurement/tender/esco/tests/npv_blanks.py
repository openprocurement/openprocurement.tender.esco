from openprocurement.tender.esco.utils import calculate_npv
from openprocurement.tender.esco.npv_calculation import (
    calculate_contract_duration,
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
