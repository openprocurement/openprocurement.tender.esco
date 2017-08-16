from openprocurement.tender.esco.utils import calculate_npv

from openprocurement.tender.esco.npv_calculation import (
    calculate_discount_coef,
)

def discount_coef(self):
    discount_rate = [4.623] + [12.500] * 19 + [7.877]
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        [0.956, 0.85, 0.756, 0.672, 0.597, 0.531, 0.472, 0.42, 0.373, 0.332, 0.295,
         0.262, 0.233, 0.207, 0.184, 0.164, 0.146, 0.13, 0.116, 0.103, 0.095]
    )

    discount_rate = [0]*21
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        [1.0]*21
    )
    
    discount_rate = [12.500] * 21
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        [0.889, 0.79, 0.702, 0.624, 0.555, 0.493, 0.438, 0.389, 0.346, 0.308,
         0.274, 0.244, 0.217, 0.193, 0.172, 0.153, 0.136, 0.121, 0.108, 0.096, 0.085]
    )