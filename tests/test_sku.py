import pytest

from src.tf2_utils import (
    get_metal,
    get_sku,
    get_sku_properties,
    is_metal,
    is_pure,
    is_sku,
    sku_is_uncraftable,
    sku_to_color,
    sku_to_defindex,
    sku_to_quality,
)
from src.tf2_utils.utils import read_json_file

file_path = "./tests/json/{}.json"


def get_item_dict(file_name: str) -> dict:
    return read_json_file(file_path.format(file_name))


CRUSADERS_CROSSBOW = get_item_dict("crusaders_crossbow")
UNCRAFTABLE_HAT = get_item_dict("uncraftable_hat")
HONG_KONG_CONE = get_item_dict("hong_kong_cone")
ELLIS_CAP = get_item_dict("ellis_cap")


def test_ellis_cap_sku() -> None:
    sku = get_sku(ELLIS_CAP)

    # https://marketplace.tf/items/tf2/263;6
    assert "263;6" == sku


def test_ellis_cap_sku_properties() -> None:
    sku = get_sku_properties(ELLIS_CAP)

    assert {
        "defindex": 263,
        "quality": 6,
        "australium": False,
        "craftable": True,
        "wear": -1,
        "killstreak_tier": -1,
        "festivized": False,
        "strange": False,
    } == sku


def test_crusaders_crossbow_sku() -> None:
    sku = get_sku(CRUSADERS_CROSSBOW)

    # https://marketplace.tf/items/tf2/305;11;kt-3;festive
    assert "305;11;kt-3;festive" == sku


def test_strange_unusual_hong_kong_cone() -> None:
    sku = get_sku(HONG_KONG_CONE)

    # https://marketplace.tf/items/tf2/30177;5;u107;strange
    assert "30177;5;u107;strange" == sku


def test_uncraftable_hat() -> None:
    sku = get_sku(UNCRAFTABLE_HAT)

    # https://marketplace.tf/items/tf2/734;6;uncraftable
    assert "734;6;uncraftable" == sku


def test_properties() -> None:
    sku = "734;6;uncraftable"

    assert 734, sku_to_defindex(sku)
    assert 6, sku_to_quality(sku)
    assert sku_is_uncraftable(sku)


def test_is_sku() -> None:
    assert is_sku("734;6;uncraftable")
    assert is_sku("something;text")
    assert not is_sku("734")


def test_is_metal() -> None:
    assert is_metal("5000;6")
    assert is_metal("5001;6")
    assert is_metal("5002;6")
    assert not is_metal("5021;6")


def test_is_pure() -> None:
    assert is_pure("5000;6")
    assert is_pure("5001;6")
    assert is_pure("5002;6")
    assert is_pure("5021;6")
    assert not is_pure("5021;7")


def test_get_metal() -> None:
    assert 9, get_metal("5002;6")
    assert 3, get_metal("5001;6")
    assert 1, get_metal("5000;6")

    with pytest.raises(AssertionError):
        get_metal("5021;6")


def test_sku_to_color() -> None:
    assert "7D6D00" == sku_to_color("734;6;uncraftable")
    assert "4D7455" == sku_to_color("30469;1")

    with pytest.raises(AssertionError):
        sku_to_color("notsku")
