# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from esculator import npv, escp
from openprocurement.api.tests.base import snitch
from openprocurement.api.utils import get_now

from openprocurement.tender.belowthreshold.tests.base import test_organization
from openprocurement.tender.belowthreshold.tests.contract import (
    TenderContractResourceTestMixin,
    TenderContractDocumentResourceTestMixin
)

from openprocurement.tender.openua.tests.contract_blanks import (
    # TenderContractResourceTest
    create_tender_contract,
    patch_tender_contract_datesigned,
)

from openprocurement.tender.esco.tests.base import (
    BaseESCOContentWebTest,
    test_tender_data,
    test_bids,
    NBU_DISCOUNT_RATE
)

from openprocurement.tender.openeu.tests.contract_blanks import (
    # TenderContractResourceTest
    contract_termination
)

from openprocurement.tender.esco.tests.contract_blanks import (
    # TenderContractResourceTest
    patch_tender_contract
)
from openprocurement.tender.esco.utils import to_decimal


contract_amountPerformance = round(to_decimal(npv(
    test_bids[0]['value']['contractDuration']['years'],
    test_bids[0]['value']['contractDuration']['days'],
    test_bids[0]['value']['yearlyPaymentsPercentage'],
    test_bids[0]['value']['annualCostsReduction'],
    get_now(),
    NBU_DISCOUNT_RATE)), 2)

contract_amount = round(to_decimal(escp(
    test_bids[0]['value']['contractDuration']['years'],
    test_bids[0]['value']['contractDuration']['days'],
    test_bids[0]['value']['yearlyPaymentsPercentage'],
    test_bids[0]['value']['annualCostsReduction'],
    get_now())), 2)


class TenderContractResourceTest(BaseESCOContentWebTest, TenderContractResourceTestMixin):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_auth = ('Basic', ('broker', ''))
    expected_contract_amountPerformance = contract_amountPerformance
    expected_contract_amount = contract_amount

    def setUp(self):
        super(TenderContractResourceTest, self).setUp()
        # Create award
        self.supplier_info = deepcopy(test_organization)
        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/awards'.format(self.tender_id), {'data': {
            'suppliers': [self.supplier_info], 'status': 'pending',
            'bid_id': self.initial_bids[0]['id'], 'value': self.initial_bids[0]['value'],
            'items': test_tender_data["items"]}})
        award = response.json['data']
        self.award_id = award['id']
        self.app.authorization = ('Basic', ('broker', ''))
        response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
            self.tender_id, self.award_id, self.tender_token), {"data": {
                "status": "active", "qualified": True, "eligible": True}})
    test_contract_termination = snitch(contract_termination)
    test_create_tender_contract = snitch(create_tender_contract)
    test_patch_tender_contract_datesigned = snitch(patch_tender_contract_datesigned)
    test_patch_tender_contract = snitch(patch_tender_contract)


class TenderContractDocumentResourceTest(BaseESCOContentWebTest,
                                         TenderContractDocumentResourceTestMixin):
    initial_status = 'active.qualification'
    initial_bids = test_bids
    initial_auth = ('Basic', ('broker', ''))

    def setUp(self):
        super(TenderContractDocumentResourceTest, self).setUp()
        # Create award
        supplier_info = deepcopy(test_organization)
        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/awards'.format(self.tender_id), {'data': {
            'suppliers': [supplier_info], 'status': 'pending',
            'bid_id': self.initial_bids[0]['id']}})
        award = response.json['data']
        self.award_id = award['id']
        response = self.app.patch_json('/tenders/{}/awards/{}'.format(
            self.tender_id, self.award_id), {"data": {
                "status": "active", "qualified": True, "eligible": True}})
        # Create contract for award
        response = self.app.post_json('/tenders/{}/contracts'.format(self.tender_id), {'data': {
            'title': 'contract title',
            'description': 'contract description',
            'awardID': self.award_id}})
        contract = response.json['data']
        self.contract_id = contract['id']
        self.app.authorization = ('Basic', ('broker', ''))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderContractResourceTest))
    suite.addTest(unittest.makeSuite(TenderContractDocumentResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
