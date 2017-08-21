from datetime import date
from openprocurement.tender.esco.tests.npv_test_data import (
    DISCOUNT_COEF,
    DISCOUNT_RATE,
    CLIENT_PAYMENT_DATA,
    CLIENT_PAYMENTS_DATA,
    DISCOUNTED_INCOME_COEF,
    INCOME_CUSTOMER,
    DISCOUNTED_INCOME_RES,
)
from openprocurement.tender.esco.constants import DAYS_PER_YEAR, NPV_CALCULATION_DURATION
from openprocurement.tender.esco.npv_calculation import (
    calculate_contract_duration,
    calculate_discount_rate,
    calculate_discount_rates,
    calculate_payment,
    calculate_payments,
    calculate_discounted_income,
    calculate_discount_coef,
    calculate_days_with_cost_reduction,
)

nbu_rate = 0.22

def discount_coef(self):
    self.assertEqual(
        calculate_discount_coef(DISCOUNT_RATE['first_test']),
        DISCOUNT_COEF['first_test']
    )

    self.assertEqual(
        calculate_discount_coef(DISCOUNT_RATE['second_test']),
        DISCOUNT_COEF['second_test']
    )

    self.assertEqual(
        calculate_discount_coef(DISCOUNT_RATE['third_test']),
        DISCOUNT_COEF['third_test']
    )


def contract_duration(self):
    # Minimal contract duration
    years = 0
    days = 1
    self.assertEqual(
        calculate_contract_duration(years, days),
        years * DAYS_PER_YEAR + days,
    )

    years = 0
    days = 364
    self.assertEqual(
        calculate_contract_duration(years, days),
        years * DAYS_PER_YEAR + days,
    )

    years = 5
    days = 275
    self.assertEqual(
        calculate_contract_duration(years, days),
        years * DAYS_PER_YEAR + days,
    )

    # Max contract duration
    years = 15
    days = 0
    self.assertEqual(
        calculate_contract_duration(years, days),
        years * DAYS_PER_YEAR + days,
    )


def discount_rate(self):
    # Predefined value
    nbu_rate = 12.5
    days = 135
    self.assertEqual(
        calculate_discount_rate(days, nbu_rate),
        4.623287671232877,
    )

    # Divide 100% by n parts and check if nbu_rate is the same as
    # nbu_rate * DAYS_PER_YEAR / DAYS_PER_YEAR
    n = 97
    for i in range(n + 1):
        nbu_rate = (i / float(n)) * 100
        days = DAYS_PER_YEAR
        self.assertEqual(
            calculate_discount_rate(days, nbu_rate, DAYS_PER_YEAR),
            nbu_rate,
        )


def discount_rates(self):
    periods = 21

    # All days for discount rate are zeros
    empty = [0] * periods
    empty_rates = calculate_discount_rates(empty, nbu_rate)
    self.assertEqual(len(empty), len(empty_rates))
    for rate in empty_rates:
        self.assertEqual(rate, 0)

    # All days for discount rate are equal to DAYS_PER_YEAR
    days = [DAYS_PER_YEAR] * periods
    calculated_rates = calculate_discount_rates(days, nbu_rate)
    self.assertEqual(len(days), len(calculated_rates))
    for rate in calculated_rates:
        self.assertEqual(rate, nbu_rate)

    # All days for discount rate are DIFFERENT
    # This code checks if calculated rates are also DIFFERENT
    days_increment = int(DAYS_PER_YEAR / periods)
    days = [(i + 1) * days_increment for i in range(21)]
    calculated_rates = calculate_discount_rates(days, nbu_rate)
    for (i, rate) in enumerate(calculated_rates):
        checking_rates = calculated_rates[i + 1:]
        for checking_rate in checking_rates:
            self.assertNotEqual(rate, checking_rate)

    # Predefined first and last value
    new_nbu_rate = 12.5
    predefined_rate1 = 4.623287671232877
    predefined_rate2 = 7.876712328767123

    days = [135] + [0] * (periods - 2) + [230]
    calculated_rates = calculate_discount_rates(days, new_nbu_rate)
    self.assertEqual(len(days), len(calculated_rates))
    self.assertEqual(calculated_rates[0], predefined_rate1)
    self.assertEqual(calculated_rates[-1], predefined_rate2)


def client_payment(self):

    # Predefined values
    yearly_payments_percentage = CLIENT_PAYMENT_DATA['yearly_percentage']
    client_cost_reduction = CLIENT_PAYMENT_DATA['client_cost_reduction']
    days_with_payments = CLIENT_PAYMENT_DATA['days_with_payments']
    days_for_discount_rate = CLIENT_PAYMENT_DATA['days_for_discount_rate']
    payment_predefined = CLIENT_PAYMENT_DATA['payment']
    prec = 2

    payment = calculate_payment(
        yearly_payments_percentage,
        client_cost_reduction,
        days_with_payments,
        days_for_discount_rate,
    )

    self.assertEqual(round(payment, prec), round(payment_predefined, prec))
    self.assertEqual(
        round(yearly_payments_percentage * client_cost_reduction, prec),
        round(payment_predefined, prec),
    )

    # No days for payments at all
    days_with_payments = 0
    payment = calculate_payment(
        yearly_payments_percentage,
        client_cost_reduction,
        days_with_payments,
        days_for_discount_rate,
    )
    self.assertEqual(payment, 0)

    # If there is more days for payments than payment must be greater
    last_payment = payment
    days_with_payments += 1
    payment = calculate_payment(
        yearly_payments_percentage,
        client_cost_reduction,
        days_with_payments,
        days_for_discount_rate,
    )
    self.assertGreater(payment, last_payment)

    # If there is less days for payments than payment must be smaller
    last_payment = payment
    days_with_payments -= 10
    payment = calculate_payment(
        yearly_payments_percentage,
        client_cost_reduction,
        days_with_payments,
        days_for_discount_rate,
    )
    self.assertLess(payment, last_payment)


def client_payments(self):

    periods = 21

    # Predefined values
    yearly_payments_percentage = CLIENT_PAYMENTS_DATA['yearly_percentage']
    client_cost_reductions = CLIENT_PAYMENTS_DATA['client_cost_reductions']
    days_with_payments = CLIENT_PAYMENTS_DATA['days_with_payments']
    days_for_discount_rate = CLIENT_PAYMENTS_DATA['days_for_discount_rate']
    payments_predefined = CLIENT_PAYMENTS_DATA['payments']
    payments_sum = CLIENT_PAYMENTS_DATA['payments_sum']
    prec = 2

    payments = calculate_payments(
        yearly_payments_percentage,
        client_cost_reductions,
        days_with_payments,
        days_for_discount_rate,
    )
    self.assertEqual(len(payments), len(client_cost_reductions))
    for i, _ in enumerate(payments):
        self.assertEqual(
            round(payments[i], prec),
            round(payments_predefined[i], prec)
        )

    self.assertEqual(round(sum(payments), prec), round(payments_sum, prec))

    # No days for payments at all
    days_with_payments = CLIENT_PAYMENTS_DATA['days_no_payments']
    days_for_discount_rate = CLIENT_PAYMENTS_DATA['full_years_discount']
    payments = calculate_payments(
        yearly_payments_percentage,
        client_cost_reductions,
        days_with_payments,
        days_for_discount_rate,
    )
    self.assertEqual(len(payments), len(client_cost_reductions))
    for payment in payments:
        self.assertEqual(payment, 0)

    # If there is more days for payments than payment must be greater
    # days_with_payments = [10, 20, ...]
    days_with_payments = CLIENT_PAYMENTS_DATA['growing_days_with_payments']
    payments = calculate_payments(
        yearly_payments_percentage,
        client_cost_reductions,
        days_with_payments,
        days_for_discount_rate,
    )
    self.assertEqual(len(payments), len(client_cost_reductions))
    for i, _ in enumerate(payments[:-1]):
        self.assertLess(
            payments[i],
            payments[i + 1],
        )


def discounted_income(self):
    self.assertEqual(
        calculate_discounted_income(DISCOUNTED_INCOME_COEF['input_data'], INCOME_CUSTOMER['first_test']),
        DISCOUNTED_INCOME_RES['first_test']
    )

    self.assertEqual(
        calculate_discounted_income(DISCOUNTED_INCOME_COEF['input_data'], INCOME_CUSTOMER['second_test']),
        DISCOUNTED_INCOME_RES['second_test']
    )


def days_with_cost_reduction(self):
    announcement_date = date(2017, 8, 18)
    self.assertEqual(
        calculate_days_with_cost_reduction(announcement_date, DAYS_PER_YEAR),
        [135] + [365] * NPV_CALCULATION_DURATION
    )

    announcement_date = date(2020, 01, 20)
    self.assertEqual(
        calculate_days_with_cost_reduction(announcement_date, DAYS_PER_YEAR),
        [346] + [365] * NPV_CALCULATION_DURATION
    )

    announcement_date = date(2019, 01, 20)
    self.assertEqual(
        calculate_days_with_cost_reduction(announcement_date, DAYS_PER_YEAR),
        [345] + [365] * NPV_CALCULATION_DURATION
    )
