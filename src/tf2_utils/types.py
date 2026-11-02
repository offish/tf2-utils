from typing import Literal, NotRequired, TypedDict

from steampie import Item

type SKU = str
type Intent = Literal["buy", "sell"]


class SKUItem(Item):
    sku: SKU


class SKUProperties(TypedDict):
    defindex: int
    quality: int
    effect: int
    australium: bool
    craftable: bool
    wear: int
    skin: int
    killstreak_tier: int
    sheen: int
    killstreaker: int
    festivized: bool
    crate_number: int
    strange: NotRequired[bool]


class MarketplaceTFItem:
    sku: str
    highest_buy_order: float
    lowest_price: float
    stock: int
