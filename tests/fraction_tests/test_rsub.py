from numbers import Real

from hypothesis import given

from cfractions import Fraction
from . import strategies


@given(strategies.finite_builtin_non_fractions, strategies.fractions)
def test_alternatives(first: Real, second: Fraction) -> None:
    result = first - second

    assert result == first + (-second)
