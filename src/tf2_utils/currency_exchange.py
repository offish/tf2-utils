from typing import Iterable

from .constants import KEY, REC, REF, SCRAP
from .item import Item
from .utils import to_scrap


def get_overview(pure: list[dict]) -> dict:
    overview = {
        KEY: 0,
        REF: 0,
        REC: 0,
        SCRAP: 0,
    }

    for item in pure:
        name = item["market_hash_name"]

        if name in overview:
            overview[name] += 1

    return overview


def get_inventory_items(combination: list[str], inventory: list[dict]) -> list[dict]:
    items = []

    for item_name in combination:
        for item in inventory:
            if item_name != item["market_hash_name"]:
                continue

            if item.get("selected"):
                continue

            items.append(item)
            item["selected"] = True
            break

    return items


def get_pure_in_inventory(inventory: list[dict]) -> list[dict]:
    items = []

    for i in inventory:
        item = Item(i)

        if item.is_tradable() and item.is_pure():
            items.append(i)

    return items


def pick_metal(
    remaining: int,
    available_refined: int,
    available_reclaimed: int,
    available_scrap: int,
) -> tuple[int, int, int] | None:
    if remaining < 0:
        return

    max_ref = min(available_refined, remaining // 9)

    for num_ref in range(max_ref, -1, -1):
        after_ref = remaining - num_ref * 9
        max_rec = min(available_reclaimed, after_ref // 3)

        for num_rec in range(max_rec, -1, -1):
            after_rec = after_ref - num_rec * 3

            if after_rec <= available_scrap:
                return num_ref, num_rec, after_rec


class CurrencyExchange:
    def __init__(
        self,
        their_inventory: list[dict],
        our_inventory: list[dict],
        intent: str,
        item_price: int,
        key_prices: dict,
        is_pure_trade: bool = False,
    ) -> None:
        if intent not in ["buy", "sell"]:
            raise ValueError(f"{intent} is not a valid intent")

        if (
            not isinstance(key_prices, dict)
            or "buy" not in key_prices
            or "sell" not in key_prices
        ):
            raise ValueError("key_prices must be a dict with buy and sell prices")

        self.their_inventory = their_inventory
        self.our_inventory = our_inventory
        self.intent = intent
        self.item_price = item_price
        self.key_prices = key_prices
        self.is_pure_trade = is_pure_trade

        self.scrap_price = item_price
        self._is_possible = False
        self.their_scrap = 0
        self.our_scrap = 0
        self.their_overview: dict[str, int] = {}
        self.our_overview: dict[str, int] = {}
        self.their_combination: list[str] = []
        self.our_combination: list[str] = []

    def _get_key_value(self, user: str) -> int:
        key_price = self.key_prices["sell"]

        if user == "them":
            key_price = self.key_prices["buy"]

        return to_scrap(key_price)

    def _get_value(self, name: str, user: str) -> int:
        value = 0

        match name:
            case "Mann Co. Supply Crate Key":
                value = self._get_key_value(user)
            case "Refined Metal":
                value = 9
            case "Reclaimed Metal":
                value = 3
            case "Scrap Metal":
                value = 1

        if not value:
            raise ValueError(f"{name} is not pure")

        return value

    def _get_total_value(self, iterable: Iterable, user: str) -> int:
        values = [i["market_hash_name"] if isinstance(i, dict) else i for i in iterable]
        return sum(self._get_value(i, user) for i in values)

    def _target_for(self, user: str) -> int:
        target = self.scrap_price

        if not self.is_pure_trade:
            if self.intent == "buy" and user == "them":
                target -= self.item_price

            if self.intent == "sell" and user == "us":
                target -= self.item_price

        return target

    def _has_enough(self) -> bool:
        return self.their_scrap >= self._target_for(
            "them"
        ) and self.our_scrap >= self._target_for("us")

    def _pick_currencies(self, user: str) -> tuple[bool, list[str]]:
        overview = self.their_overview if user == "them" else self.our_overview
        target = self._target_for(user)
        key_price = self._get_key_value(user)

        if target < 0:
            return False, []

        if target == 0:
            return True, []

        available_keys = overview[KEY]
        available_refined = overview[REF]
        available_reclaimed = overview[REC]
        available_scrap = overview[SCRAP]
        max_keys = min(available_keys, target // key_price)

        for num_keys in range(max_keys, -1, -1):
            remaining = target - num_keys * key_price
            combo = pick_metal(
                remaining, available_refined, available_reclaimed, available_scrap
            )

            if combo is None:
                continue

            num_ref, num_rec, num_scrap = combo
            combination = (
                [KEY] * num_keys
                + [REF] * num_ref
                + [REC] * num_rec
                + [SCRAP] * num_scrap
            )
            return True, combination

        return False, []

    def _set_combinations(self) -> bool:
        success_their, their_combination = self._pick_currencies("them")
        success_our, our_combination = self._pick_currencies("us")

        if not success_their or not success_our:
            return False

        self.their_combination = their_combination
        self.our_combination = our_combination

        return True

    def _adds_up(self) -> bool:
        their_value = self._get_total_value(self.their_combination, "them")
        our_value = self._get_total_value(self.our_combination, "us")

        if not self.is_pure_trade:
            if self.intent == "buy":
                their_value += self.item_price

            if self.intent == "sell":
                our_value += self.item_price

        return their_value == our_value

    def calculate(self) -> None:
        their_pure = get_pure_in_inventory(self.their_inventory)
        our_pure = get_pure_in_inventory(self.our_inventory)

        self.their_scrap = self._get_total_value(their_pure, "them")
        self.our_scrap = self._get_total_value(our_pure, "us")
        self.their_overview = get_overview(their_pure)
        self.our_overview = get_overview(our_pure)

        while self._has_enough():
            if self._set_combinations():
                if self._adds_up():
                    self._is_possible = True

                return

            self.scrap_price += 1

    def get_their_items(self) -> list[dict]:
        assert self._is_possible, "Currencies does not add up"
        return get_inventory_items(self.their_combination, self.their_inventory)

    def get_our_items(self) -> list[dict]:
        assert self._is_possible, "Currencies does not add up"
        return get_inventory_items(self.our_combination, self.our_inventory)

    def get_currencies(self) -> tuple[list[dict], list[dict]]:
        return (self.get_their_items(), self.get_our_items())

    @property
    def is_possible(self) -> bool:
        return self._is_possible
