import pytest

from src.tf2_utils import (
    is_half_scrap_price,
    refinedify,
    swap_intent,
    to_refined,
    to_scrap,
)


def test_to_refined() -> None:
    assert to_refined(43) == 4.77


def test_to_scrap() -> None:
    assert to_scrap(2.44) == 22


def test_refinedify() -> None:
    assert refinedify(32.53) == 32.55
    assert refinedify(12.47) == 12.44


def test_swap_intent() -> None:
    assert swap_intent("buy") == "sell"
    assert swap_intent("BUY") == "sell"
    assert swap_intent("sell") == "buy"
    assert swap_intent("Sell") == "buy"

    with pytest.raises(AssertionError):
        swap_intent("asdf")


@pytest.mark.parametrize(
    "metal,value",
    [
        (0.05, True),
        (0.16, True),
        (0.27, True),
        (0.38, True),
        (0.5, True),
        (0.61, True),
        (0.72, True),
        (0.83, True),
        (0.94, True),
        (0.11, False),
        (0.22, False),
        (0.33, False),
        (0.44, False),
        (0.55, False),
        (0.66, False),
        (0.77, False),
        (0.88, False),
        (1.0, False),
        (1.11, False),
    ],
)
def test_half_scrap_price(metal: float, value: bool) -> None:
    assert is_half_scrap_price(metal) is value
