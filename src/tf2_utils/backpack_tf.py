import requests

from dataclasses import dataclass, asdict


__all__ = [
    "Currencies",
    "Enity",
    "ItemResolvable",
    "ItemDocument",
    "ListingResolvable",
    "Listing",
    "BackpackTF",
]


@dataclass
class Currencies:
    keys: int = 0
    metal: float = 0.0


@dataclass
class Enity:
    name: str
    id: int
    color: str


@dataclass
class ItemResolvable:
    item: str
    quality: str | int
    tradable: bool
    craftable: str
    priceindex: str


@dataclass
class ItemDocument:
    baseName: str
    name: str
    imageUrl: str
    quantity: int
    quality: Enity
    rarity: Enity
    paint: Enity
    particle: Enity
    elevatedQuality: Enity


@dataclass
class ListingResolvable:
    id: int  # asset_id if this is set, its a sell order
    item: dict
    details: str
    currencies: Currencies


@dataclass
class Listing:
    id: str
    appid: int
    bumpedAt: str
    listedAt: str
    details: str
    intent: str
    steamid: str
    currencies: Currencies
    promoted: bool
    tradeOffersPreferred: bool
    count: int
    item: ItemDocument


class BackpackTFException(Exception):
    pass


class NeedsAPIKey(BackpackTFException):
    pass


class BackpackTF:
    URL = "https://backpack.tf/api"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.user_token = None

    def _get_request(self, endpoint: str, params: dict = {}) -> dict:
        if self.api_key:
            params["apiKey"] = self.api_key

        response = requests.get(self.URL + endpoint, params=params)
        return response.json()

    def _post_request(self, endpoint: str, json: dict = {}) -> dict:
        if self.api_key:
            json["apiKey"] = self.api_key

        response = requests.post(self.URL + endpoint, json=json)
        return response.json()

    def _delete_request(self, endpoint: str, params: dict = {}) -> dict:
        if self.api_key:
            params["apiKey"] = self.api_key

        response = requests.delete(self.URL + endpoint, params=params)
        return response.json()

    def _patch_request(self, endpoint: str, params: dict = {}) -> dict:
        if self.api_key:
            params["apiKey"] = self.api_key

        response = requests.patch(self.URL + endpoint, params=params)
        return response.json()

    def get_listings(self, skip: int = 0, limit: int = 100) -> dict:
        return self._get_request(
            "/v2/classifieds/listings", {"skip": skip, "limit": limit}
        )

    def create_listing(self, listing: ListingResolvable) -> Listing:
        return self._post_request("/v2/classifieds/listings", asdict(listing))

    def make_listing(
        self, id: int, item: dict, details: str, currencies: dict
    ) -> Listing:
        listing = ListingResolvable(id, item, details, Currencies(**currencies))
        return self.create_listing(listing)


if __name__ == "__main__":
    # BackpackTF.create_listing(ListingResolvable(1, 1, 1, 1, 1))

    # listin = ListingResolvable("1", {}, "my details", Currencies(1, 1.5))
    # listin = ListingResolvable(
    #     "1", {}, "my details", Currencies(**{"keys": 1, "metal": 1.5})
    # )
    listin = ListingResolvable("1", {}, "my details", Currencies(**{"keys": 2}))
    print(asdict(listin))
    # curren = Currencies(1, 1.5)
    # print(curren.__dict__)
