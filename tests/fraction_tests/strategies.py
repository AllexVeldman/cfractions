import math
from numbers import Rational

from hypothesis import strategies

from cfractions import Fraction

zero_integers = strategies.just(0)
small_integers = strategies.integers(1, 5)
precisions = strategies.none() | strategies.integers(-10, 10)
integers = numerators = strategies.integers()
integers_64 = strategies.integers(min_value=-2 ** 63, max_value=2 ** 63 - 1)
negative_integers = strategies.integers(max_value=-1)
positive_integers = strategies.integers(min_value=1)
denominators = non_zero_integers = negative_integers | positive_integers


def is_not_interned(value: int) -> bool:
    return value is not int(str(value))


non_interned_numerators = non_interned_denominators = (
    (strategies.integers(max_value=-256)
     | strategies.integers(min_value=257)).filter(is_not_interned))
floats = strategies.floats(allow_infinity=True,
                           allow_nan=True)
finite_negative_floats = strategies.floats(max_value=0,
                                           exclude_max=True,
                                           allow_infinity=False,
                                           allow_nan=False)
non_zero_floats = floats.filter(bool)
zero_floats = strategies.sampled_from([-0., 0.])
small_non_negative_integral_floats = small_integers.map(float)
finite_floats = strategies.floats(allow_infinity=False,
                                  allow_nan=False)
finite_non_zero_floats = finite_floats.filter(bool)
infinite_floats = strategies.sampled_from([math.inf, -math.inf])
nans = strategies.just(math.nan)
non_fractions = integers | floats
finite_non_fractions = integers | finite_floats
zero_fractions = strategies.builds(Fraction)
fractions = (strategies.builds(Fraction, numerators, denominators)
             | strategies.builds(Fraction, finite_floats))
negative_fractions = strategies.builds(Fraction, negative_integers,
                                       positive_integers)
int64_fractions = strategies.builds(Fraction, integers_64, denominators)
non_zero_fractions = strategies.builds(Fraction, non_zero_integers,
                                       denominators)
small_positive_integral_fractions = strategies.builds(Fraction, small_integers)
small_non_negative_integral_fractions = (zero_fractions
                                         | small_positive_integral_fractions)
non_zero_rationals = non_zero_integers | non_zero_fractions
zero_non_fractions = zero_integers | zero_floats
zero_numbers = zero_non_fractions | zero_fractions
rationals = integers | fractions
finite_numbers = rationals | finite_floats
finite_non_zero_numbers = (non_zero_integers | finite_non_zero_floats
                           | non_zero_fractions)
non_integer_numbers = floats | fractions
finite_negative_numbers = (negative_integers | finite_negative_floats
                           | negative_fractions)


@Rational.register
class CustomRational:
    def __init__(self, numerator: int, denominator: int) -> None:
        self.denominator, self.numerator = denominator, numerator

    def __repr__(self) -> str:
        return (type(self).__qualname__ + '(' + str(self.numerator) + ', '
                + str(self.denominator) + ')')


custom_rationals = strategies.builds(CustomRational, numerators, denominators)
