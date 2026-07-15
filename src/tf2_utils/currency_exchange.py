from .constants import KEY, REC, REF, SCRAP
from .item import Item

METAL_VALUES = {
    REF: 9,
    REC: 3,
    SCRAP: 1,
}


class CurrencyExchange:
    def __init__(
        self,
        their_inventory: list[dict],
        our_inventory: list[dict],
        intent: str,
        item_price: int,
        key_price: int,
        item_is_not_pure: bool = True,
    ) -> None:
        if intent not in ("buy", "sell"):
            raise ValueError(f"{intent} is not a valid intent")

        self.their_inventory = their_inventory
        self.our_inventory = our_inventory

        self.is_buying = intent == "buy"
        self.is_selling = intent == "sell"

        self.item_price = item_price
        self.scrap_price = item_price
        self.key_price = key_price
        self.item_is_not_pure = item_is_not_pure

        self._is_possible = False
        self.their_scrap = 0
        self.our_scrap = 0
        self.their_overview: dict[str, int] = {}
        self.our_overview: dict[str, int] = {}
        self.their_combination: list[str] = []  # list of metal names
        self.our_combination: list[str] = []  # list of metal names

    def get_pure_value(self, name: str) -> int:
        if name == KEY:
            return self.key_price

        if name in METAL_VALUES:
            return METAL_VALUES[name]

        raise ValueError(f"{name} is not pure")

    def get_pure_in_inventory(self, inventory: list[dict]) -> tuple[int, list[dict]]:
        scrap = 0
        metal = []

        for item in inventory:
            item_util = Item(item)
            name = item["market_hash_name"]

            if not item_util.is_tradable():
                continue

            if not item_util.is_pure():
                continue

            pure_value = self.get_pure_value(name)
            item["pure_value"] = pure_value

            scrap += pure_value
            metal.append(item)

        return scrap, metal

    @staticmethod
    def format_overview(pure: list[dict]) -> dict:
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

    @staticmethod
    def _overview_to_items(combination: list[str], inventory: list[dict]) -> list[dict]:
        items = []

        for metal_name in combination:
            for item in inventory:
                if item["market_hash_name"] != metal_name:
                    continue

                if item.get("picked"):
                    continue

                items.append(item)
                item["picked"] = True
                break

        return items

    def get_currencies(self) -> tuple[list[dict], list[dict]]:
        assert self._is_possible, "Currencies does not add up"

        their_items = self._overview_to_items(
            self.their_combination, self.their_inventory
        )
        our_items = self._overview_to_items(self.our_combination, self.our_inventory)

        return their_items, our_items

    def _target_for(self, user: str) -> int:
        target = self.scrap_price

        if self.item_is_not_pure:
            if self.is_buying and user == "them":
                target -= self.item_price

            if self.is_selling and user == "us":
                target -= self.item_price

        return target

    def _has_enough(self) -> bool:
        return self.their_scrap >= self._target_for(
            "them"
        ) and self.our_scrap >= self._target_for("us")

    @staticmethod
    def _make_metal(
        remaining: int, available_ref: int, available_rec: int, available_scrap: int
    ) -> tuple[int, int, int] | None:
        if remaining < 0:
            return None

        max_ref = min(available_ref, remaining // 9)

        for num_ref in range(max_ref, -1, -1):
            after_ref = remaining - num_ref * 9
            max_rec = min(available_rec, after_ref // 3)

            for num_rec in range(max_rec, -1, -1):
                after_rec = after_ref - num_rec * 3

                if after_rec <= available_scrap:
                    return num_ref, num_rec, after_rec

        return None

    def _pick_currencies(self, user: str) -> tuple[bool, list[str]]:
        overview = self.their_overview if user == "them" else self.our_overview
        target = self._target_for(user)

        if target < 0:
            return False, []

        if target == 0:
            return True, []

        available_keys = overview[KEY]
        available_ref = overview[REF]
        available_rec = overview[REC]
        available_scrap = overview[SCRAP]

        max_keys = (
            min(available_keys, target // self.key_price) if self.key_price > 0 else 0
        )

        for num_keys in range(max_keys, -1, -1):
            remaining = target - num_keys * self.key_price
            combo = self._make_metal(
                remaining, available_ref, available_rec, available_scrap
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
        their_value = sum(self.get_pure_value(name) for name in self.their_combination)
        our_value = sum(self.get_pure_value(name) for name in self.our_combination)

        if self.item_is_not_pure:
            if self.is_buying:
                their_value += self.item_price

            if self.is_selling:
                our_value += self.item_price

        return their_value == our_value

    def calculate(self) -> None:
        self.their_scrap, their_pure = self.get_pure_in_inventory(self.their_inventory)
        self.our_scrap, our_pure = self.get_pure_in_inventory(self.our_inventory)

        self.their_overview = self.format_overview(their_pure)
        self.our_overview = self.format_overview(our_pure)

        while self._has_enough():
            if self._set_combinations():
                if self._adds_up():
                    self._is_possible = True

                return

            self.scrap_price += 1

    @property
    def is_possible(self) -> bool:
        return self._is_possible
