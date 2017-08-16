import unittest
from openprocurement.api.tests.base import snitch

from openprocurement.tender.esco.tests.npv_blanks import (
    contract_duration,
    discount_rate,
    discount_rates,
    client_payment,
    client_payments,
)


class NPVCalculationTest(unittest.TestCase):
    """ NPV Calculation Test
        based on data from https://docs.google.com/spreadsheets/d/1kOz6bxob4Nmb0Es_W0TmbNznoYDcnwAKcSgxfPEXYGQ/edit#gid=1469973930
    """

    test_contract_duration = snitch(contract_duration)
    test_discount_rate = snitch(discount_rate)
    test_discount_rates = snitch(discount_rates)
    test_client_payment = snitch(client_payment)
    test_client_payments = snitch(client_payments)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NPVCalculationTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
