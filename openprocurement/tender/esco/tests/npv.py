import unittest
from openprocurement.api.tests.base import snitch

from openprocurement.tender.esco.tests.npv_blanks import (
    days_with_cost_reduction,
    contract_duration,
    days_for_discount_rate,
)


class NPVCalculationTest(unittest.TestCase):
    """ NPV Calculation Test
        based on data from https://docs.google.com/spreadsheets/d/1kOz6bxob4Nmb0Es_W0TmbNznoYDcnwAKcSgxfPEXYGQ/edit#gid=1469973930
    """
    test_days_with_cost_reduction = snitch(days_with_cost_reduction)
    test_contract_duration = snitch(contract_duration)
    test_days_for_discount_rate = snitch(days_for_discount_rate)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NPVCalculationTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
