from fractions import Fraction

from openprocurement.tender.esco.utils import calculate_npv

from openprocurement.tender.esco.npv_calculation import (
    calculate_discount_coef,
)

def discount_coef(self):
    discount_rate = [Fraction(str(4.623))]+[Fraction(str(12.500))]*19 + [Fraction(str(7.877))]
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        [Fraction(100000, 104623), Fraction(800000, 941607), Fraction(6400000, 8474463), Fraction(51200000, 76270167),
         Fraction(409600000, 686431503), Fraction(3276800000, 6177883527), Fraction(26214400000, 55600951743),
         Fraction(209715200000, 500408565687), Fraction(1677721600000, 4503677091183),
         Fraction(13421772800000, 40533093820647), Fraction(107374182400000, 364797844385823),
         Fraction(858993459200000, 3283180599472407), Fraction(6871947673600000, 29548625395251663),
         Fraction(54975581388800000, 265937628557264967), Fraction(439804651110400000, 2393438657015384703),
         Fraction(3518437208883200000, 21540947913138462327), Fraction(28147497671065600000, 193868531218246160943),
         Fraction(225179981368524800000, 1744816780964215448487),
         Fraction(1801439850948198400000, 15703351028677939036383),
         Fraction(14411518807585587200000, 141330159258101451327447),
         Fraction(1441151880758558720000000000, 15246273590286210264851000019)]

    )

    discount_rate = [Fraction(str(0))]*21
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        [Fraction(1, 1)]*21

    )

    discount_rate = [Fraction(str(12.500))] * 21
    self.assertEqual(
        calculate_discount_coef(discount_rate),
        [Fraction(8, 9), Fraction(64, 81), Fraction(512, 729), Fraction(4096, 6561), Fraction(32768, 59049),
         Fraction(262144, 531441), Fraction(2097152, 4782969), Fraction(16777216, 43046721),
         Fraction(134217728, 387420489), Fraction(1073741824, 3486784401), Fraction(8589934592, 31381059609),
         Fraction(68719476736, 282429536481), Fraction(549755813888, 2541865828329),
         Fraction(4398046511104, 22876792454961), Fraction(35184372088832, 205891132094649),
         Fraction(281474976710656, 1853020188851841), Fraction(2251799813685248, 16677181699666569),
         Fraction(18014398509481984, 150094635296999121), Fraction(144115188075855872, 1350851717672992089),
         Fraction(1152921504606846976, 12157665459056928801), Fraction(9223372036854775808, 109418989131512359209)]

    )