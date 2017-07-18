# -*- coding: utf-8 -*-
from datetime import timedelta

from openprocurement.api.utils import get_now
from openprocurement.tender.belowthreshold.tests.base import test_organization


def award_items_without_quantity_deliveryDate(self):

    auth = self.app.authorization
    self.app.authorization = ('Basic', ('token', ''))
    bid = self.initial_bids[0]
    response = self.app.post_json('/tenders/{}/awards'.format(
        self.tender_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': bid['id'],
                                   'lotID': bid['lotValues'][0]['relatedLot'],
                                   "items": [
                                       {
                                           "description": u"футляри до державних нагород",
                                           "description_en": u"Cases for state awards",
                                           "classification": {
                                               "scheme": u"CPV",
                                               "id": u"44617100-9",
                                               "description": u"Cartons"
                                           },
                                           "additionalClassifications": [
                                               {
                                                   "scheme": u"ДКПП",
                                                   "id": u"17.21.1",
                                                   "description": u"папір і картон гофровані, паперова й картонна тара"
                                               }
                                           ],
                                           "unit": {
                                               "name": u"item",
                                               "code": u"44617100-9"
                                           },
                                           "quantity": 5,
                                           "deliveryDate": {
                                               "startDate": (get_now() + timedelta(days=2)).isoformat(),
                                               "endDate": (get_now() + timedelta(days=5)).isoformat()
                                           },

                                           "deliveryAddress": {
                                               "countryName": u"Україна",
                                               "postalCode": "79000",
                                               "region": u"м. Київ",
                                               "locality": u"м. Київ",
                                               "streetAddress": u"вул. Банкова 1"
                                           }
                                       }
                                   ]
                                   }})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']
    self.new_award_id = award['id']

    for item in award['items']:
        self.assertNotIn('deliveryDate', item)
        self.assertNotIn('quantity', item)

    response = self.app.patch_json(
        '/tenders/{}/awards/{}'.format(self.tender_id, award['id']),
        {"data": {'status': 'active', "qualified": True, "eligible": True,
                  "items": [{'quantity': 10,
                             'deliveryDate': {
                                "startDate": (get_now() + timedelta(days=12)).isoformat(),
                                "endDate": (get_now() + timedelta(days=15)).isoformat()
                             }}]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.get('/tenders/{}/awards/{}'.format(self.tender_id, self.new_award_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']

    for item in award['items']:
        self.assertNotIn('deliveryDate', item)
        self.assertNotIn('quantity', item)
    self.app.authorization = auth

    response = self.app.patch_json(
        '/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, self.award_id, self.tender_token),
        {"data": {'status': 'active', "qualified": True, "eligible": True,
                  "items": [{
                               "description": u"футляри до державних нагород",
                               "description_en": u"Cases for state awards",
                               "classification": {
                                   "scheme": u"CPV",
                                   "id": u"44617100-9",
                                   "description": u"Cartons"
                               },
                               "additionalClassifications": [
                                   {
                                       "scheme": u"ДКПП",
                                       "id": u"17.21.1",
                                       "description": u"папір і картон гофровані, паперова й картонна тара"
                                   }
                               ],
                               "unit": {
                                   "name": u"item",
                                   "code": u"44617100-9"
                               },
                               "quantity": 5,
                               "deliveryDate": {
                                   "startDate": (get_now() + timedelta(days=2)).isoformat(),
                                   "endDate": (get_now() + timedelta(days=5)).isoformat()
                               },
                               "deliveryAddress": {
                                   "countryName": u"Україна",
                                   "postalCode": "79000",
                                   "region": u"м. Київ",
                                   "locality": u"м. Київ",
                                   "streetAddress": u"вул. Банкова 1"
                               }
                           }]}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotIn('items', response.json['data'])
