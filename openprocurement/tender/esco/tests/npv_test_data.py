from fractions import Fraction


DISCOUNT_COEF = {'first_test': [Fraction(100000, 104623), Fraction(800000, 941607), Fraction(6400000, 8474463),
                            Fraction(51200000, 76270167), Fraction(409600000, 686431503), Fraction(3276800000, 6177883527),
                            Fraction(26214400000, 55600951743), Fraction(209715200000, 500408565687),
                            Fraction(1677721600000, 4503677091183), Fraction(13421772800000, 40533093820647),
                            Fraction(107374182400000, 364797844385823), Fraction(858993459200000, 3283180599472407),
                            Fraction(6871947673600000, 29548625395251663), Fraction(54975581388800000, 265937628557264967),
                            Fraction(439804651110400000, 2393438657015384703), Fraction(3518437208883200000, 21540947913138462327),
                            Fraction(28147497671065600000, 193868531218246160943), Fraction(225179981368524800000, 1744816780964215448487),
                            Fraction(1801439850948198400000, 15703351028677939036383), Fraction(14411518807585587200000, 141330159258101451327447),
                            Fraction(1441151880758558720000000000, 15246273590286210264851000019)],

                 'second_test': [Fraction(1, 1)]*21,

                 'third_test': [Fraction(8, 9), Fraction(64, 81), Fraction(512, 729), Fraction(4096, 6561), Fraction(32768, 59049),
                                Fraction(262144, 531441), Fraction(2097152, 4782969), Fraction(16777216, 43046721),
                                Fraction(134217728, 387420489), Fraction(1073741824, 3486784401), Fraction(8589934592, 31381059609),
                                Fraction(68719476736, 282429536481), Fraction(549755813888, 2541865828329), Fraction(4398046511104, 22876792454961),
                                Fraction(35184372088832, 205891132094649), Fraction(281474976710656, 1853020188851841),
                                Fraction(2251799813685248, 16677181699666569), Fraction(18014398509481984, 150094635296999121),
                                Fraction(144115188075855872, 1350851717672992089), Fraction(1152921504606846976, 12157665459056928801),
                                Fraction(9223372036854775808, 109418989131512359209)]
                 }

DISCOUNT_RATE = {'first_test': [Fraction(str(0.04623))]+[Fraction(str(0.125))]*19 + [Fraction(str(0.07877))],
                 'second_test': [Fraction(str(0))]*21,
                 'third_test': [Fraction(str(0.12500))] * 21
                 }

DISCOUNTED_INCOME_COEF = {'input_data': [Fraction(str(0.956)),
                          Fraction(str(0.850)), Fraction(str(0.755)),
                          Fraction(str(0.671)), Fraction(str(0.597)),
                          Fraction(str(0.530)), Fraction(str(0.471)),
                          Fraction(str(0.419)), Fraction(str(0.373)),
                          Fraction(str(0.331)), Fraction(str(0.294)),
                          Fraction(str(0.262)), Fraction(str(0.233)),
                          Fraction(str(0.207)), Fraction(str(0.184)),
                          Fraction(str(0.163)), Fraction(str(0.145)),
                          Fraction(str(0.129)), Fraction(str(0.115)),
                          Fraction(str(0.102)), Fraction(str(0.095))]
                          }
INCOME_CUSTOMER = {'first_test': [Fraction(str(27.74))]+[Fraction(str(75.00))]+[Fraction(str(91.78))] +
                                 [Fraction(str(139.73))]+[Fraction(str(250.00))]*16+[Fraction(str(157.53))],

                   'second_test': [Fraction(str(0.095))]*21
                   }

DISCOUNTED_INCOME_RES = {'first_test':[Fraction(331493, 12500), Fraction(255, 4), Fraction(692939, 10000),
                                       Fraction(9375883, 100000), Fraction(597, 4), Fraction(265, 2), Fraction(471, 4),
                                       Fraction(419, 4), Fraction(373, 4), Fraction(331, 4), Fraction(147, 2),
                                       Fraction(131, 2), Fraction(233, 4), Fraction(207, 4), Fraction(46, 1),
                                       Fraction(163, 4),  Fraction(145, 4), Fraction(129, 4), Fraction(115, 4),
                                       Fraction(51, 2), Fraction(299307, 20000)],

                         'second_test': [Fraction(4541, 50000), Fraction(323, 4000), Fraction(2869, 40000),
                                         Fraction(12749, 200000), Fraction(11343, 200000), Fraction(1007, 20000),
                                         Fraction(8949, 200000), Fraction(7961, 200000), Fraction(7087, 200000),
                                         Fraction(6289, 200000), Fraction(2793, 100000), Fraction(2489, 100000),
                                         Fraction(4427, 200000), Fraction(3933, 200000), Fraction(437, 25000),
                                         Fraction(3097, 200000), Fraction(551, 40000), Fraction(2451, 200000),
                                         Fraction(437, 40000), Fraction(969, 100000), Fraction(361, 40000)]

                         }

COST_REDUCTIONS = {'first_test':[Fraction("92.47")] + [Fraction("250.0")] * 20}
PAYMENTS = {'first_test':[Fraction("64.73"), Fraction("175.0"), Fraction("175.0"), Fraction("110.27")] + [Fraction("0.0")] * 17}
EXPECTED_INCOME = {'first_test':[Fraction("27.74"), Fraction("75.0"), Fraction("75.0"), Fraction("139.73")] + [Fraction("250.0")] * 17}
