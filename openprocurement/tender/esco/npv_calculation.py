from openprocurement.tender.esco.constants import DAYS_PER_YEAR
from fractions import Fraction


def calculate_contract_duration(
        contract_duration_years,
        contract_duration_days,
        days_per_year=DAYS_PER_YEAR):
    '''Calculate contract duration in days'''

    return contract_duration_years * days_per_year + contract_duration_days


def calculate_discount_rate(
        days_for_discount_rate,
        nbu_discount_rate,
        days_per_year=DAYS_PER_YEAR):
    '''Calculate discount rate according to the law'''

    return float(Fraction(nbu_discount_rate) *
                 Fraction(days_for_discount_rate, days_per_year))


def calculate_discount_rates(
        days_for_discount_rates,
        nbu_discount_rate,
        days_per_year=DAYS_PER_YEAR):
    '''Calculate discount rates from days_for_discount_rates list'''

    return [
        calculate_discount_rate(
            days_for_discount_rate,
            nbu_discount_rate,
            days_per_year,
        ) for days_for_discount_rate in days_for_discount_rates
    ]


def calculate_payment(
        yearly_payments_percentage,
        client_cost_reduction,
        days_with_payments,
        days_for_discount_rate):
    '''Calculates client payment to a participant'''

    if days_with_payments > 0:
        # Transormation Fraction(str(float)) is done because of its
        # better precision than Fraction(float).
        #
        # For example:
        # >>> Fraction(str(0.2))
        # Fraction(1, 5)
        # >>> Fraction(0.2)
        # Fraction(3602879701896397, 18014398509481984)

        yearly_payments_percentage = Fraction(
            Fraction(str(yearly_payments_percentage)),
            100
        )
        client_cost_reduction = Fraction(str(client_cost_reduction))

        return (yearly_payments_percentage * client_cost_reduction *
                Fraction(days_with_payments, days_for_discount_rate))
    return 0


def calculate_payments(
        yearly_payments_percentage,
        client_cost_reductions,
        days_with_payments,
        days_for_discount_rate):
    '''Calculates client payments to a participant'''

    lists = zip(
        client_cost_reductions,
        days_with_payments,
        days_for_discount_rate,
    )

    return map(
        lambda arg: calculate_payment(yearly_payments_percentage, *arg),
        lists,
    )
