from fractions import Fraction
from openprocurement.tender.esco.tests.npv_test_data import DISCOUNT_COEF
from openprocurement.tender.esco.npv_calculation import (
    calculate_discount_coef,
)



def discount_coef(self):
    discount_rate = [Fraction(str(0.04623))]+[Fraction(str(0.125))]*19 + [Fraction(str(0.07877))]
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        DISCOUNT_COEF['first_test']
    )

    discount_rate = [Fraction(str(0))]*21
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        DISCOUNT_COEF['second_test']
    )

    discount_rate = [Fraction(str(0.12500))] * 21
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        DISCOUNT_COEF['third_test']
    )
