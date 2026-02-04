from aiohttp import ClientSession

from .instances import schema
from .sku import sku_is_craftable, sku_to_quality_name


class MarketplaceTF:
    def __init__(self, session: ClientSession) -> None:
        self.session = session

    @staticmethod
    def format_url(item_name: str, quality: str, craftable: bool) -> str:
        url = "https://api.backpack.tf/item/get_third_party_prices"
        craftable = "Craftable" if craftable else "Non-Craftable"
        return f"{url}/{quality}/{item_name}/Tradable/{craftable}"

    def format_url_sku(self, sku: str) -> str:
        item_name = schema.sku_to_base_name(sku)
        quality = sku_to_quality_name(sku)
        return self.format_url(item_name, quality, sku_is_craftable(sku))

    @staticmethod
    def format_price_to_float(price: str | float) -> float:
        if isinstance(price, float):
            return price

        return float(price.replace("$", ""))

    async def fetch_item(self, sku: str) -> dict:
        url = self.format_url_sku(sku)

        async with self.session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.json()

        prices = data["prices"]["mp"]
        highest_buy_order = prices["highest_buy_order"]
        lowest_price = prices["lowest_price"]
        stock = int(prices["num_for_sale"])

        return {
            "sku": prices["sku"],
            "highest_buy_order": self.format_price_to_float(highest_buy_order),
            "lowest_price": self.format_price_to_float(lowest_price),
            "stock": stock,
        }
