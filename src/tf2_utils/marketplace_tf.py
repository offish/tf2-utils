import time

import requests

from .exceptions import TF2UtilsError
from .schema import SchemaItemsUtils
from .sku import sku_is_craftable, sku_to_quality_name


class MarketplaceTFException(TF2UtilsError):
    pass


class SKUDoesNotMatch(MarketplaceTFException):
    pass


class NoAPIKey(MarketplaceTFException):
    pass


def api_key_required(func):
    def wrapper(self, *args, **kwargs):
        if self._api_key is None:
            raise NoAPIKey("No API key provided")

        return func(self, *args, **kwargs)

    return wrapper


class MarketplaceTF:
    def __init__(self, api_key: str = None):
        self._api_key = api_key
        self._schema = SchemaItemsUtils()
        self._data = {}

    def _get_request(self, endpoint: str, params: dict = {}) -> dict:
        url = "https://marketplace.tf/api" + endpoint

        if self._api_key is not None:
            params["key"] = self._api_key

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def get_endpoints(self) -> dict:
        return self._get_request("/Meta/GetEndpoints/v1")

    @api_key_required
    def get_bots(self) -> dict:
        return self._get_request("/Bots/GetBots/v2")

    @api_key_required
    def get_bans(self, steam_id: str) -> dict:
        return self._get_request("/Bans/GetUserBan/v2", {"steamid": steam_id})

    def get_is_banned(self, steam_id: str) -> bool:
        return self.get_bans(steam_id)["result"][0]["banned"]

    def get_name(self, steam_id: str) -> str:
        return self.get_bans(steam_id)["result"][0]["name"]

    def get_is_seller(self, steam_id: str) -> bool:
        return self.get_bans(steam_id)["result"][0]["seller"]

    def get_seller_id(self, steam_id: str) -> int:
        return self.get_bans(steam_id)["result"][0]["id"]

    @api_key_required
    def get_dashboard_items(self) -> dict:
        return self._get_request("/Seller/GetDashboardItems/v2")

    @api_key_required
    def get_sales(self, number: int = 100, start_before: int = 0) -> dict:
        if start_before == 0:
            start_before = int(time.time())

        return self._get_request(
            "/Seller/GetSales/v2", {"num": number, "start_before": start_before}
        )

    @staticmethod
    def _format_url(item_name: str, quality: str, craftable: bool) -> str:
        url = "https://api.backpack.tf/item/get_third_party_prices"
        craftable = "Craftable" if craftable else "Non-Craftable"

        return f"{url}/{quality}/{item_name}/Tradable/{craftable}"

    def _format_url_sku(self, sku: str) -> str:
        item_name = self._schema.sku_to_base_name(sku)
        quality = sku_to_quality_name(sku)

        return self._format_url(item_name, quality, sku_is_craftable(sku))

    @staticmethod
    def _format_price_to_float(price: str | float) -> float:
        if isinstance(price, float):
            return price

        return float(price.replace("$", ""))

    def _set_data(self, data: dict) -> None:
        self._data = data["prices"]["mp"]

    def fetch_item_raw(self, item_name: str, quality: str, craftable: bool) -> dict:
        url = self._format_url(item_name, quality, craftable)
        self._set_data(requests.get(url).json())

        return self._data

    def fetch_item(self, sku: str) -> dict:
        url = self._format_url_sku(sku)
        self._set_data(requests.get(url).json())
        mptf_sku = self.get_sku()

        if mptf_sku != sku:
            raise SKUDoesNotMatch(f"SKU {sku} does not match {mptf_sku}")

        return self._data

    def get_item_data(self) -> dict:
        return self._data

    def get_lowest_price(self) -> float:
        price = self._data.get("lowest_price", 0.0)
        return self._format_price_to_float(price)

    def get_price(self) -> float:
        return self.get_lowest_price()

    def get_highest_buy_order(self) -> float:
        price = self._data.get("highest_buy_order", 0.0)
        return self._format_price_to_float(price)

    def get_buy_order(self) -> float:
        return self.get_highest_buy_order()

    def get_stock(self) -> int:
        return self._data.get("num_for_sale", 0)

    def get_sku(self) -> str:
        return self._data.get("sku", "")

    def fetch_lowest_price(self, sku: str) -> float:
        price = self.fetch_item(sku).get("lowest_price", 0.0)
        return self._format_price_to_float(price)

    def fetch_price(self, sku: str) -> float:
        return self.fetch_lowest_price(sku)

    def fetch_highest_buy_order(self, sku: str) -> float:
        price = self.fetch_item(sku).get("highest_buy_order")
        return self._format_price_to_float(price)

    def fetch_buy_order(self, sku: str) -> float:
        return self.fetch_highest_buy_order(sku)

    def fetch_stock(self, sku: str) -> int:
        return self.fetch_item(sku).get("num_for_sale", 0)
