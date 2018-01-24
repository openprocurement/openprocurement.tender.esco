import unittest
from openprocurement.tender.core.tests.configurator import ConfiguratorTestMixin
from openprocurement.tender.esco.adapters import TenderESCOConfigurator
from openprocurement.tender.esco.models import Tender


class ConfiguratorTest(unittest.TestCase, ConfiguratorTestMixin):
    configurator_class = TenderESCOConfigurator
    reverse_awarding_criteria = True
    awarding_criteria_key = 'amountPerfomance'
    configurator_model = Tender


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConfiguratorTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
