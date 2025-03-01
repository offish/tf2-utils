from .item import Item


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
        self.their_inventory = their_inventory
        self.our_inventory = our_inventory

        if intent not in ["buy", "sell"]:
            raise ValueError(f"{intent} is not a valid intent")

        self.is_buying = intent == "buy"
        self.is_selling = intent == "sell"
        self.item_price = item_price
        self.scrap_price = item_price
        self.key_price = key_price
        self.item_is_not_pure = item_is_not_pure

        self._is_possible = False
        self.their_scrap = 0
        self.our_scrap = 0
        self.their_overview = {}
        self.our_overview = {}
        self.their_combination = []  # list of metal names
        self.our_combination = []  # list of metal names

    def get_pure_value(self, name: str) -> int:
        if name == "Mann Co. Supply Crate Key":
            return self.key_price

        if name == "Refined Metal":
            return 9

        if name == "Reclaimed Metal":
            return 3

        if name == "Scrap Metal":
            return 1

        raise ValueError(f"{name} is not pure")

    def get_pure_in_inventory(self, inventory: list[dict]) -> tuple[int, list[dict]]:
        """scrap value, list of metal item dicts"""
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

    @staticmethod
    def format_overview(pure: list[dict]) -> dict:
        overview = {
            "Mann Co. Supply Crate Key": 0,
            "Refined Metal": 0,
            "Reclaimed Metal": 0,
            "Scrap Metal": 0,
        }

        for item in pure:
            for pure_name in overview:
                if item["market_hash_name"] != pure_name:
                    continue

                overview[pure_name] += 1
                break

        return overview

    def _pick_currencies(self, user: str) -> tuple[bool, list[str]]:
        """ref, ref, scrap, rec"""
        overview = (
            self.their_overview.copy() if user == "them" else self.our_overview.copy()
        )
        price = self.scrap_price

        combination = []

        if self.is_buying and user == "them" and self.item_is_not_pure:
            price -= self.item_price

        if self.is_selling and user == "us" and self.item_is_not_pure:
            price -= self.item_price

        while price != 0:
            did_add = False

            for name in overview:
                value = self.get_pure_value(name)

                if overview[name] == 0:
                    continue

                if price % value != 0:
                    continue

                # goes from key->ref->rec->scrap will pick most expensieve
                # currency available first
                price -= value
                overview[name] -= 1
                combination.append(name)
                did_add = True

                break

            if not did_add:
                return False, []

        return True, combination

    def _adds_up(self) -> bool:
        their_value = 0
        our_value = 0

        for name in self.their_combination:
            their_value += self.get_pure_value(name)

        for name in self.our_combination:
            our_value += self.get_pure_value(name)

        if self.is_buying and self.item_is_not_pure:
            their_value += self.item_price

        if self.is_selling and self.item_is_not_pure:
            our_value += self.item_price

        return their_value == our_value

    def _set_combinations(self) -> bool:
        success_our, our_combination = self._pick_currencies("us")
        success_their, their_combination = self._pick_currencies("them")

        if not success_our or not success_their:
            return False

        self.our_combination = our_combination
        self.their_combination = their_combination

        return True

    def _has_enough(self) -> bool:
        temp_price = self.scrap_price

        if self.item_is_not_pure:
            temp_price -= self.item_price

        if self.is_buying:
            return self.their_scrap >= temp_price and self.our_scrap >= self.scrap_price

        return self.their_scrap >= self.scrap_price and self.our_scrap >= temp_price

    def calculate(self) -> None:
        self.their_scrap, their_pure = self.get_pure_in_inventory(self.their_inventory)
        self.our_scrap, our_pure = self.get_pure_in_inventory(self.our_inventory)

        self.their_overview = self.format_overview(their_pure)
        self.our_overview = self.format_overview(our_pure)

        if not self._has_enough():
            return

        while self._has_enough():
            success = self._set_combinations()

            if success:
                break

            # since we could not find a combination, we add 1 scrap to each side and
            # try again, do this till we have either user does not have enough anymore
            self.scrap_price += 1

        if not self._adds_up():
            return

        # everything adds up and looks good
        self._is_possible = True

    @property
    def is_possible(self) -> bool:
        return self._is_possible
