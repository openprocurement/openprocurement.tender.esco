from fractions import Fraction
DISCOUNT_RATE = [4.623]+[12.500]*19 + [7.877]

def calculate_discount_coef( discount_rate = DISCOUNT_RATE):
    discount_coef = []
    coefficient = Fraction(1)
    for i in discount_rate:
        coefficient = Fraction(coefficient, (Fraction(Fraction(str(i)), Fraction(100))+Fraction(1)))
        discount_coef.append(float(coefficient))
    return discount_coef
