from collections import Counter
from typing import Optional

from src.tf2_utils import KEY, REC, REF, SCRAP, CurrencyExchange
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


def pure(*names: str) -> list[dict]:
    return [{"market_hash_name": name, "tags": TAG} for name in names]


def overview(
    key: int = 0, refined: int = 0, reclaimed: int = 0, scrap: int = 0
) -> dict:
    return {
        KEY: key,
        REF: refined,
        REC: reclaimed,
        SCRAP: scrap,
    }


def item_names(items: list[dict]) -> Counter:
    return Counter(item["market_hash_name"] for item in items)


def run(
    their_inventory: list[dict],
    our_inventory: list[dict],
    intent: str,
    item_price: int,
    *,
    item_is_not_pure: bool = True,
    their_scrap: int,
    our_scrap: int,
    possible: bool,
    their_overview: Optional[dict] = None,
    our_overview: Optional[dict] = None,
    their_combination: Optional[Counter] = None,
    our_combination: Optional[Counter] = None,
) -> None:
    c = CurrencyExchange(
        their_inventory,
        our_inventory,
        intent,
        item_price,
        KEY_RATE,
        item_is_not_pure,
    )
    c.calculate()

    assert c.their_scrap == their_scrap
    assert c.our_scrap == our_scrap
    assert c.is_possible == possible

    if their_overview is not None:
        assert c.their_overview == their_overview

    if our_overview is not None:
        assert c.our_overview == our_overview

    if their_combination is not None:
        assert Counter(c.their_combination) == their_combination

    if our_combination is not None:
        assert Counter(c.our_combination) == our_combination


def test_rounding_makes_it_impossible() -> None:
    run(
        pure(REF, REC, SCRAP, REF),
        pure(REF, REC),
        "buy",
        4,
        their_scrap=22,
        our_scrap=12,
        their_overview=overview(refined=2, reclaimed=1, scrap=1),
        our_overview=overview(refined=1, reclaimed=1),
        possible=False,
    )


def test_not_enough_value() -> None:
    run(
        pure(REF, REF, SCRAP),
        [],
        "sell",
        20,
        their_scrap=19,
        our_scrap=0,
        possible=False,
    )


def test_enough_value_but_no_combination() -> None:
    run(
        pure(REF, REF),
        pure(REC, REF),
        "buy",
        17,
        their_scrap=18,
        our_scrap=12,
        possible=False,
    )


def test_buyer_overpays_and_gets_scrap_change() -> None:
    run(
        pure(REF, SCRAP, SCRAP, SCRAP, SCRAP, SCRAP, SCRAP),
        pure(REF, REC),
        "buy",
        4,
        their_scrap=15,
        our_scrap=12,
        their_overview=overview(refined=1, scrap=6),
        our_overview=overview(refined=1, reclaimed=1),
        possible=True,
        their_combination=Counter({SCRAP: 5}),
        our_combination=Counter({REF: 1}),
    )


def test_buyer_pays_exact_price_using_a_key() -> None:
    run(
        pure(REF, SCRAP, KEY, SCRAP, SCRAP, SCRAP, SCRAP, REC, REC),
        pure(REF, REF),
        "sell",
        14,
        their_scrap=KEY_RATE + 20,
        our_scrap=18,
        their_overview=overview(key=1, refined=1, reclaimed=2, scrap=5),
        our_overview=overview(refined=2),
        possible=True,
        their_combination=Counter({REF: 1, REC: 1, SCRAP: 2}),
        our_combination=Counter(),
    )


def test_pure_for_pure_trade_ignores_item_price() -> None:
    run(
        pure(SCRAP, SCRAP, SCRAP, REC, REC),
        pure(REF, REF),
        "buy",
        9,
        item_is_not_pure=False,
        their_scrap=9,
        our_scrap=18,
        their_overview=overview(reclaimed=2, scrap=3),
        our_overview=overview(refined=2),
        possible=True,
        their_combination=Counter({REC: 2, SCRAP: 3}),
        our_combination=Counter({REF: 1}),
    )


def test_real_inventory() -> None:
    mapped_inventory = map_inventory(INVENTORY, True)

    c = CurrencyExchange(mapped_inventory, [], "sell", 15, KEY_RATE)
    c.calculate()

    assert c.their_scrap == 591
    assert c.our_scrap == 0
    assert c.their_overview == overview(refined=65, reclaimed=1, scrap=3)
    assert c.our_overview == overview()
    assert c.is_possible
    assert Counter(c.their_combination) == Counter({REF: 1, REC: 1, SCRAP: 3})
    assert c.our_combination == []

    their_items, our_items = c.get_currencies()

    assert item_names(their_items) == item_names(PICKED_METALS)
    assert our_items == []
