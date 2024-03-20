from .schema import SchemaItemsUtils
from .sku import sku_to_quality_name, sku_is_craftable

import requests


class SKUDoesNotMatch(Exception):
    pass


class MarketplaceTF:
    def __init__(self):
        self.schema = SchemaItemsUtils()
        self.data = {}

    @staticmethod
    def _format_url(item_name: str, quality: str, craftable: bool) -> str:
        url = "https://api.backpack.tf/item/get_third_party_prices/"
        craftable = "Craftable" if craftable else "Non-Craftable"

        return f"{url}/{quality}/{item_name}/Tradable/{craftable}"

    def _format_url_sku(self, sku: str) -> str:
        item_name = self.schema.sku_to_base_name(sku)
        quality = sku_to_quality_name(sku)

        return self._format_url(item_name, quality, sku_is_craftable(sku))

    @staticmethod
    def _format_price_to_float(price: str) -> float:
        return float(price.replace("$", ""))

    def _set_data(self, data: dict) -> None:
        self.data = data["prices"]["mp"]

    def fetch_item_raw(self, item_name: str, quality: str, craftable: bool) -> dict:
        url = self._format_url(item_name, quality, craftable)
        self._set_data(requests.get(url).json())

        return self.data

    def fetch_item(self, sku: str) -> dict:
        url = self._format_url_sku(sku)
        self._set_data(requests.get(url).json())
        mptf_sku = self.get_sku()

        if mptf_sku != sku:
            raise SKUDoesNotMatch(f"SKU {sku} does not match {mptf_sku}")

        return self.data

    def get_item_data(self) -> dict:
        return self.data

    def get_lowest_price(self) -> float:
        price = self.data.get("lowest_price")

        if price is None:
            return 0.0

        return self._format_price_to_float(price)

    def get_price(self) -> float:
        return self.get_lowest_price()

    def get_highest_buy_order(self) -> float:
        price = self.data.get("highest_buy_order")

        if price is None:
            return 0.0

        return self._format_price_to_float(price)

    def get_buy_order(self) -> float:
        return self.get_highest_buy_order()

    def get_stock(self) -> int:
        return self.data.get("num_for_sale", 0)

    def get_sku(self) -> str:
        return self.data.get("sku", "")

    def fetch_lowest_price(self, sku: str) -> float:
        price = self.fetch_item_data(sku).get("lowest_price")

        if price is None:
            return 0.0

        return self._format_price_to_float(price)

    def fetch_price(self, sku: str) -> float:
        return self.fetch_lowest_price(sku)

    def fetch_highest_buy_order(self, sku: str) -> float:
        price = self.fetch_item_data(sku).get("highest_buy_order")

        if price is None:
            return 0.0

        return self._format_price_to_float(price)

    def fetch_buy_order(self, sku: str) -> float:
        return self.fetch_highest_buy_order(sku)

    def fetch_stock(self, sku: str) -> int:
        return self.fetch_item_data(sku).get("num_for_sale", 0)

    # {"prices":{"mp":{"sku":"357;6;kt-2","lowest_price":"$1.85","num_for_sale":5}}}
