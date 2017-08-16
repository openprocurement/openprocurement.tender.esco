from fractions import Fraction
DISCOUNT_RATE = [Fraction(str(4.623))]+[Fraction(str(12.500))]*19 + [Fraction(str(7.877))]

def calculate_discount_coef(discount_rate = DISCOUNT_RATE):
    discount_coef = []
    coefficient = Fraction(1)
    for i in discount_rate:
        coefficient = Fraction(coefficient, (Fraction(i, Fraction(100))+Fraction(1)))
        discount_coef.append(coefficient)
    return discount_coef
