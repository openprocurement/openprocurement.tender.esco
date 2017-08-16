from openprocurement.tender.esco.utils import calculate_npv
from openprocurement.tender.esco.constants import DAYS_PER_YEAR
from openprocurement.tender.esco.npv_calculation import (
    calculate_contract_duration,
    calculate_discount_rate,
    calculate_discount_rates,
    calculate_payment,
)


nbu_rate = 0.22


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
    yearly_payments_percentage = 70.0
    client_cost_reduction = 92.47
    days_with_payments = 135
    days_for_discount_rate = 135
    payment_predefined = 64.73
    prec = 2

    payment = calculate_payment(
        yearly_payments_percentage,
        client_cost_reduction,
        days_with_payments,
        days_for_discount_rate,
    )

    self.assertEqual(round(payment, prec), round(payment_predefined, prec))
    self.assertEqual(
        round(yearly_payments_percentage * client_cost_reduction / 100, prec),
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
