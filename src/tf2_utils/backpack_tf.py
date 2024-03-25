import requests

from dataclasses import dataclass, field

from .schema import SchemaItemsUtils
from .sku import sku_to_quality, sku_is_craftable
from . import __title__


__all__ = [
    "Currencies",
    "Enity",
    # "ItemResolvable",
    "ItemDocument",
    "Listing",
    "BackpackTF",
]


@dataclass
class Currencies:
    keys: int = 0
    metal: float = 0.0


@dataclass
class Enity:
    name: str = ""
    id: int = 0
    color: str = ""


@dataclass
class ItemDocument:
    appid: int
    baseName: str
    defindex: int
    id: str
    imageUrl: str
    marketName: str
    name: str
    # origin:None
    originalId: str
    price: dict
    quality: Enity
    summary: str
    # class:list
    slot: str
    tradable: bool
    craftable: bool


@dataclass
class ItemResolvable:
    baseName: str
    craftable: bool
    quality: Enity
    tradable: bool = True


@dataclass
class Listing:
    id: str
    steamid: str
    appid: int
    currencies: Currencies
    value: dict
    tradeOffersPreferred: bool
    buyoutOnly: bool
    details: str
    listedAt: int
    bumpedAt: int
    intent: str
    count: int
    status: str
    source: str
    item: ItemDocument
    user: dict
    userAgent: dict = field(default_factory=dict)


class BackpackTFException(Exception):
    pass


class NeedsAPIKey(BackpackTFException):
    pass


class BackpackTF:
    URL = "https://api.backpack.tf/api"

    def __init__(
        self, token: str, api_key: str = "", user_agent="listed with <3"
    ) -> None:
        self.token = token
        self.api_key = api_key
        self.user_agent = user_agent
        self.user_token = None
        self.schema = SchemaItemsUtils()

        self.__headers = {"User-Agent": f"{__title__} | {self.user_agent}"}

    def request(self, method: str, endpoint: str, params: dict = {}, **kwargs) -> dict:
        params["token"] = self.token
        response = requests.request(
            method, self.URL + endpoint, params=params, headers=self.__headers, **kwargs
        )
        return response.json()

    def get_listings(self, skip: int = 0, limit: int = 100) -> dict:
        return self._get_request(
            "/v2/classifieds/listings", {"skip": skip, "limit": limit}
        )

    def _construct_listing_item(self, sku: str) -> dict:
        return {
            "baseName": self.schema.sku_to_base_name(sku),
            "craftable": sku_is_craftable(sku),
            "tradable": True,
            "quality": {"id": sku_to_quality(sku)},
        }

    def _construct_listing(
        self, sku: str, intent: str, currencies: dict, details: str, asset_id: int = 0
    ) -> dict:
        listing = {
            "item": self._construct_listing_item(sku),
            "details": details,
            "currencies": Currencies(**currencies).__dict__,
        }

        if intent == "sell":
            listing["id"] = asset_id

        return listing

    def create_listing(
        self, sku: str, intent: str, currencies: dict, details: str, asset_id: int = 0
    ) -> Listing:
        listing = self._construct_listing(sku, intent, currencies, details, asset_id)
        response = self.request("POST", "/v2/classifieds/listings", json=listing)

        return Listing(**response)

    def register_user_agent(self) -> dict:
        return self.request("POST", "/agent/pulse")
