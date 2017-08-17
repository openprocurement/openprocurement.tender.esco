from fractions import Fraction


def calculate_discount_coef(discount_rate):
    discount_coef = []
    coefficient = Fraction(1)
    for i in discount_rate:
        coefficient = Fraction(coefficient, (i+Fraction(1)))
        discount_coef.append(coefficient)
    return discount_coef
