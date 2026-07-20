from collections import Counter

from src.tf2_utils import KEY, REC, REF, SCRAP, CurrencyExchange
from src.tf2_utils.inventory import map_inventory
from src.tf2_utils.utils import read_json_file

KEY_PRICES = {"buy": 55.77, "sell": 56}


def pure(*names: str) -> list[dict]:
    return [
        {
            "market_hash_name": name,
            "tags": [
                {
                    "category": "Quality",
                    "internal_name": "Unique",
                    "localized_category_name": "Quality",
                    "localized_tag_name": "Unique",
                    "color": "7D6D00",
                }
            ],
        }
        for name in names
    ]


def overview(
    key: int = 0, refined: int = 0, reclaimed: int = 0, scrap: int = 0
) -> dict:
    return {
        KEY: key,
        REF: refined,
        REC: reclaimed,
        SCRAP: scrap,
    }


def run(
    their_inventory: list[dict],
    our_inventory: list[dict],
    intent: str,
    item_price: int,
    *,
    is_pure_trade: bool = False,
    their_overview: dict | None = None,
    our_overview: dict | None = None,
    their_scrap: int,
    our_scrap: int,
    possible: bool,
    their_combination: Counter | None = None,
    our_combination: Counter | None = None,
) -> None:
    currency = CurrencyExchange(
        their_inventory,
        our_inventory,
        intent,
        item_price,
        KEY_PRICES,
        is_pure_trade,
    )
    currency.calculate()

    assert currency.their_scrap == their_scrap
    assert currency.our_scrap == our_scrap
    assert currency.is_possible == possible

    if their_overview is not None:
        assert currency.their_overview == their_overview

    if our_overview is not None:
        assert currency.our_overview == our_overview

    if their_combination is not None:
        assert Counter(currency.their_combination) == their_combination

    if our_combination is not None:
        assert Counter(currency.our_combination) == our_combination


def test_rounding() -> None:
    run(
        pure(REF, REC, SCRAP, REF),
        pure(REF, REC),
        "buy",
        4,
        their_overview=overview(refined=2, reclaimed=1, scrap=1),
        our_overview=overview(refined=1, reclaimed=1),
        their_scrap=22,
        our_scrap=12,
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


def test_buyer_gets_change() -> None:
    run(
        pure(REF, SCRAP, SCRAP, SCRAP, SCRAP, SCRAP, SCRAP),
        pure(REF, REC),
        "buy",
        4,
        their_overview=overview(refined=1, scrap=6),
        our_overview=overview(refined=1, reclaimed=1),
        their_scrap=15,
        our_scrap=12,
        possible=True,
        their_combination=Counter({SCRAP: 5}),
        our_combination=Counter({REF: 1}),
    )


def test_buyer_pays_exact_price() -> None:
    run(
        pure(REF, SCRAP, KEY, SCRAP, SCRAP, SCRAP, SCRAP, REC, REC),
        pure(REF, REF),
        "sell",
        14,
        their_overview=overview(key=1, refined=1, reclaimed=2, scrap=5),
        our_overview=overview(refined=2),
        their_scrap=522,
        our_scrap=18,
        possible=True,
        their_combination=Counter({REF: 1, REC: 1, SCRAP: 2}),
        our_combination=Counter(),
    )


def test_pure_only_trade() -> None:
    run(
        pure(SCRAP, SCRAP, SCRAP, REC, REC),
        pure(REF, REF),
        "buy",
        9,
        is_pure_trade=True,
        their_overview=overview(reclaimed=2, scrap=3),
        our_overview=overview(refined=2),
        their_scrap=9,
        our_scrap=18,
        possible=True,
        their_combination=Counter({REC: 2, SCRAP: 3}),
        our_combination=Counter({REF: 1}),
    )


def test_buyer_uses_one_key() -> None:
    run(
        pure(KEY, KEY, REF),
        [],
        "sell",
        511,
        their_scrap=1013,
        our_scrap=0,
        their_overview=overview(key=2, refined=1),
        our_overview=overview(),
        possible=True,
        their_combination=Counter({KEY: 1, REF: 1}),
        our_combination=Counter(),
    )


def test_buy_has_enough_metal_not_keys() -> None:
    inventory = [REF] * 58 + [REC, REC, SCRAP]

    run(
        pure(*inventory),
        pure(REC, REC, SCRAP, SCRAP),
        "sell",
        523,
        their_overview=overview(refined=58, reclaimed=2, scrap=1),
        our_overview=overview(reclaimed=2, scrap=2),
        their_scrap=529,
        our_scrap=8,
        possible=True,
        their_combination=Counter({REF: 58, SCRAP: 1}),
        our_combination=Counter(),
    )


def test_real_inventory() -> None:
    inventory = read_json_file("./tests/json/inventory.json")
    mapped_inventory = map_inventory(inventory, True)
    currency = CurrencyExchange(mapped_inventory, [], "sell", 15, KEY_PRICES)
    currency.calculate()

    assert currency.their_overview == overview(refined=65, reclaimed=1, scrap=3)
    assert currency.our_overview == overview()
    assert currency.their_scrap == 591
    assert currency.our_scrap == 0
    assert currency.is_possible
    assert Counter(currency.their_combination) == Counter({REF: 1, REC: 1, SCRAP: 3})
    assert currency.our_combination == []
