import requests

from dataclasses import dataclass, field
from hashlib import md5

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
    tradeOffersPreferred: bool = None
    buyoutOnly: bool = None


class BackpackTFException(Exception):
    pass


class NoTokenProvided(BackpackTFException):
    pass


class NeedsAPIKey(BackpackTFException):
    pass


def needs_token(func):
    def wrapper(self, *args, **kwargs):
        if not self.token:
            raise NoTokenProvided("Set a token to use this method")

        return func(self, *args, **kwargs)

    return wrapper


class BackpackTF:
    URL = "https://api.backpack.tf/api"

    def __init__(
        self, token: str, steam_id: str, api_key: str = "", user_agent="listed with <3"
    ) -> None:
        self.token = token
        self.steam_id = steam_id
        self.api_key = api_key
        self.user_agent = user_agent
        self.user_token = None
        self.schema = SchemaItemsUtils()

        self.__headers = {"User-Agent": f"{__title__} | {self.user_agent}"}

    @needs_token
    def request(self, method: str, endpoint: str, params: dict = {}, **kwargs) -> dict:
        params["token"] = self.token
        response = requests.request(
            method, self.URL + endpoint, params=params, headers=self.__headers, **kwargs
        )
        return response.json()

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
        if intent not in ["buy", "sell"]:
            raise BackpackTFException(f"Invalid intent {intent} must be buy or sell")

        listing = {
            "item": self._construct_listing_item(sku),
            "buyout": True,
            "offers": True,
            "promoted": False,
            "details": details,
            "currencies": Currencies(**currencies).__dict__,
        }

        if intent == "sell":
            listing["id"] = asset_id

        return listing

    def get_listings(self, skip: int = 0, limit: int = 100) -> dict:
        return self.request(
            "GET", "/v2/classifieds/listings", {"skip": skip, "limit": limit}
        )

    def create_listing(
        self, sku: str, intent: str, currencies: dict, details: str, asset_id: int = 0
    ) -> Listing:
        listing = self._construct_listing(sku, intent, currencies, details, asset_id)
        response = self.request("POST", "/v2/classifieds/listings", json=listing)

        return Listing(**response)

    def create_listings(self, listings: list[dict]) -> list[Listing]:
        listings = [self._construct_listing(**listing) for listing in listings]
        response = self.request("POST", "/v2/classifieds/listings/batch", json=listings)
        return [Listing(**listing["result"]) for listing in response]

    def delete_all_listings(self) -> dict:
        return self.request("DELETE", "/v2/classifieds/listings")

    def delete_listing(self, listing_id: str) -> dict:
        return self.request("DELETE", f"/v2/classifieds/listings/{listing_id}")

    @staticmethod
    def _get_item_hash(item_name: str) -> str:
        return md5(item_name.encode()).hexdigest()

    def _get_sku_item_hash(self, sku: str) -> str:
        item_name = self.schema.sku_to_full_name(sku)
        return self._get_item_hash(item_name)

    def delete_listing_by_asset_id(self, asset_id: int) -> dict:
        listing_id = f"440_{asset_id}"
        return self.delete_listing(listing_id)

    def delete_listing_by_sku(self, sku: str) -> dict:
        item_hash = self._get_sku_item_hash(sku)
        listing_id = f"440_{self.steam_id}_{item_hash}"
        return self.delete_listing(listing_id)

    def register_user_agent(self) -> dict:
        return self.request("POST", "/agent/pulse")

    def get_user_agent_status(self) -> dict:
        return self.request("POST", "/agent/status")

    def stop_user_agent(self) -> dict:
        return self.request("POST", "/agent/stop")
