from src.tf2_utils.currency import CurrencyExchange
from src.tf2_utils.inventory import map_inventory
from src.tf2_utils.utils import read_json_file

INVENTORY = read_json_file("./tests/json/inventory.json")
PICKED_METALS = read_json_file("./tests/json/picked_metals.json")

KEY_RATE = 56 * 9
TAG = [
    {
        "category": "Quality",
        "internal_name": "Unique",
        "localized_category_name": "Quality",
        "localized_tag_name": "Unique",
        "color": "7D6D00",
    }
]


def test_utils() -> None:
    c = CurrencyExchange(
        [
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Reclaimed Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Refined Metal", "tags": TAG},
        ],
        [
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Reclaimed Metal", "tags": TAG},
        ],
        "buy",
        4,
        KEY_RATE,
    )
    c.calculate()

    assert 22 == c.their_scrap
    assert 12 == c.our_scrap

    assert {
        "Mann Co. Supply Crate Key": 0,
        "Refined Metal": 2,
        "Reclaimed Metal": 1,
        "Scrap Metal": 1,
    } == c.their_overview
    assert {
        "Mann Co. Supply Crate Key": 0,
        "Refined Metal": 1,
        "Reclaimed Metal": 1,
        "Scrap Metal": 0,
    } == c.our_overview

    assert not c.is_possible


def test_not_enough() -> None:
    c = CurrencyExchange(
        [
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
        ],
        [],
        "sell",
        20,
        KEY_RATE,
    )
    c.calculate()

    assert 19 == c.their_scrap
    assert not c.is_possible


def test_no_combination() -> None:
    c = CurrencyExchange(
        [
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Refined Metal", "tags": TAG},
        ],
        [
            {"market_hash_name": "Reclaimed Metal", "tags": TAG},
            {"market_hash_name": "Refined Metal", "tags": TAG},
        ],
        "buy",
        17,  # 1.88
        KEY_RATE,
    )
    c.calculate()

    assert 18 == c.their_scrap
    assert 12 == c.our_scrap

    # they have enough but there is no combo which would work
    assert not c.is_possible


def test_possible() -> None:
    c = CurrencyExchange(
        [
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
        ],
        [
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Reclaimed Metal", "tags": TAG},
        ],
        "buy",
        4,
        KEY_RATE,
    )
    c.calculate()

    assert 15 == c.their_scrap
    assert 12 == c.our_scrap

    assert {
        "Mann Co. Supply Crate Key": 0,
        "Refined Metal": 1,
        "Reclaimed Metal": 0,
        "Scrap Metal": 6,
    } == c.their_overview
    assert {
        "Mann Co. Supply Crate Key": 0,
        "Refined Metal": 1,
        "Reclaimed Metal": 1,
        "Scrap Metal": 0,
    } == c.our_overview

    assert c.is_possible

    # 0.44, but we pay 1 ref
    # that means they have to add 0.55
    assert ["Refined Metal"] == c.our_combination
    assert [
        "Scrap Metal",
        "Scrap Metal",
        "Scrap Metal",
        "Scrap Metal",
        "Scrap Metal",
    ] == c.their_combination


def test_best_possible() -> None:
    c = CurrencyExchange(
        [
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Mann Co. Supply Crate Key", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Reclaimed Metal", "tags": TAG},
            {"market_hash_name": "Reclaimed Metal", "tags": TAG},
        ],
        [
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Refined Metal", "tags": TAG},
        ],
        "sell",
        14,
        KEY_RATE,
    )
    c.calculate()

    assert KEY_RATE + 20 == c.their_scrap
    assert 18 == c.our_scrap

    assert {
        "Mann Co. Supply Crate Key": 1,
        "Refined Metal": 1,
        "Reclaimed Metal": 2,
        "Scrap Metal": 5,
    } == c.their_overview
    assert {
        "Mann Co. Supply Crate Key": 0,
        "Refined Metal": 2,
        "Reclaimed Metal": 0,
        "Scrap Metal": 0,
    } == c.our_overview

    assert c.is_possible

    assert [
        "Scrap Metal",
        "Scrap Metal",
        "Reclaimed Metal",
        "Refined Metal",
    ] == c.their_combination
    assert [] == c.our_combination


def test_only_metal() -> None:
    c = CurrencyExchange(
        [
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Scrap Metal", "tags": TAG},
            {"market_hash_name": "Reclaimed Metal", "tags": TAG},
            {"market_hash_name": "Reclaimed Metal", "tags": TAG},
        ],
        [
            {"market_hash_name": "Refined Metal", "tags": TAG},
            {"market_hash_name": "Refined Metal", "tags": TAG},
        ],
        "buy",
        9,
        KEY_RATE,
        False,
    )
    c.calculate()

    assert 9 == c.their_scrap
    assert 18 == c.our_scrap

    assert {
        "Mann Co. Supply Crate Key": 0,
        "Refined Metal": 0,
        "Reclaimed Metal": 2,
        "Scrap Metal": 3,
    } == c.their_overview
    assert {
        "Mann Co. Supply Crate Key": 0,
        "Refined Metal": 2,
        "Reclaimed Metal": 0,
        "Scrap Metal": 0,
    } == c.our_overview

    assert c.is_possible

    assert [
        "Reclaimed Metal",
        "Reclaimed Metal",
        "Scrap Metal",
        "Scrap Metal",
        "Scrap Metal",
    ] == c.their_combination
    assert ["Refined Metal"] == c.our_combination


def test_real_inventory() -> None:
    mapped_inventory = map_inventory(INVENTORY, True)

    c = CurrencyExchange(
        mapped_inventory,
        [],
        "sell",
        15,
        KEY_RATE,
    )

    c.calculate()

    assert 591 == c.their_scrap
    assert 0 == c.our_scrap

    assert {
        "Mann Co. Supply Crate Key": 0,
        "Refined Metal": 65,
        "Reclaimed Metal": 1,
        "Scrap Metal": 3,
    } == c.their_overview
    assert {
        "Mann Co. Supply Crate Key": 0,
        "Refined Metal": 0,
        "Reclaimed Metal": 0,
        "Scrap Metal": 0,
    } == c.our_overview

    assert c.is_possible

    assert [
        "Reclaimed Metal",
        "Scrap Metal",
        "Scrap Metal",
        "Scrap Metal",
        "Refined Metal",
    ] == c.their_combination
    assert [] == c.our_combination

    their_items, our_items = c.get_currencies()

    assert PICKED_METALS == their_items
    assert [] == our_items
