import pytest

from src.tf2_utils import get_metal, get_sku, get_sku_properties, sku_to_color


def test_ellis_cap_sku_properties(ellis_cap: dict) -> None:
    assert get_sku_properties(ellis_cap) == {
        "defindex": 263,
        "quality": 6,
        "australium": False,
        "craftable": True,
        "wear": -1,
        "killstreak_tier": -1,
        "festivized": False,
        "strange": False,
    }


def test_strange_part_sku_properties(strange_part: dict) -> None:
    assert get_sku_properties(strange_part) == {
        "defindex": 6012,
        "quality": 6,
        "australium": False,
        "craftable": True,
        "wear": -1,
        "killstreak_tier": -1,
        "festivized": False,
        "strange": False,
    }


def test_get_sku_items(
    ellis_cap: dict,
    crusaders_crossbow: dict,
    hong_kong_cone: dict,
    uncraftable_hat: dict,
    strange_part: dict,
) -> None:
    # https://marketplace.tf/items/tf2/263;6
    assert get_sku(ellis_cap) == "263;6"
    # https://marketplace.tf/items/tf2/305;11;kt-3;festive
    assert get_sku(crusaders_crossbow) == "305;11;kt-3;festive"
    # https://marketplace.tf/items/tf2/30177;5;u107;strange
    assert get_sku(hong_kong_cone) == "30177;5;u107;strange"
    # https://marketplace.tf/items/tf2/734;6;uncraftable
    assert get_sku(uncraftable_hat) == "734;6;uncraftable"
    # https://marketplace.tf/items/tf2/6012;6
    assert get_sku(strange_part) == "6012;6"


def test_get_metal() -> None:
    assert get_metal("5002;6") == 9
    assert get_metal("5001;6") == 3
    assert get_metal("5000;6") == 1

    with pytest.raises(AssertionError):
        get_metal("5021;6")


def test_sku_to_color() -> None:
    assert sku_to_color("734;6;uncraftable") == "7D6D00"
    assert sku_to_color("30469;1") == "4D7455"

    with pytest.raises(AssertionError):
        sku_to_color("notsku")
