import unittest
from openprocurement.api.tests.base import snitch

from openprocurement.tender.esco.tests.npv_blanks import (
    contract_duration,
    discount_rate,
    discount_rates,
    days_with_cost_reduction,
    days_for_discount_rate,
    days_with_payments,
    income,
)


class NPVCalculationTest(unittest.TestCase):
    """ NPV Calculation Test
        based on data from https://docs.google.com/spreadsheets/d/1kOz6bxob4Nmb0Es_W0TmbNznoYDcnwAKcSgxfPEXYGQ/edit#gid=1469973930
    """

    test_contract_duration = snitch(contract_duration)
    test_days_with_cost_reduction = snitch(days_with_cost_reduction)
    test_days_for_discount_rate = snitch(days_for_discount_rate)
    test_discount_rate = snitch(discount_rate)
    test_discount_rates = snitch(discount_rates)
    test_days_with_payments = snitch(days_with_payments)
    test_client_income = snitch(income)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NPVCalculationTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
