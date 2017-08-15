
DISCOUNT_RATE = [4.623, 12.500, 12.500, 12.500, 12.500, 12.500, 12.500, 12.500, 12.500, 12.500, 12.500,
                 12.500, 12.500, 12.500, 12.500, 12.500, 12.500, 12.500, 12.500, 12.500, 7.877]

def calculate_discount_coef( discount_rate = DISCOUNT_RATE):
    discount_coef = []
    coefficient = 1
    for i in discount_rate:
        res = round((float(coefficient)/(i/100+1)),3)
        coefficient = res
        discount_coef.append(res)
    return discount_coef
