DISCOUNT_RATE = [4.623]+[12.500]*19 + [7.877]

def calculate_discount_coef( discount_rate = DISCOUNT_RATE):
    discount_coef = []
    coefficient = 1
    for i in discount_rate:
        coefficient = round((float(coefficient)/(i/100+1)), 3)
        discount_coef.append(coefficient)
    return discount_coef