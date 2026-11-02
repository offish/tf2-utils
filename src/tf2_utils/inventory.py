from collections.abc import Iterable

from steampie import InventoryResponse
from steampie import Item as ItemDict
from tf2_sku import is_key, is_metal

from .exceptions import InvalidInventory
from .sku import get_metal, get_sku
from .types import SKU, SKUItem


def yield_sku(mapped_inventory: list[SKUItem]) -> Iterable[SKU]:
    for item in mapped_inventory:
        yield item["sku"]


def map_inventory(
    inventory: InventoryResponse, add_skus: bool = False, skip_untradable: bool = False
) -> list[SKUItem | ItemDict]:
    mapped_inventory = []

    if inventory.get("assets") is None:
        raise InvalidInventory("No assets found in inventory")

    if inventory.get("descriptions") is None:
        raise InvalidInventory("No descriptions found in inventory")

    description_lookup = {}

    for description in inventory["descriptions"]:
        if skip_untradable and not description["tradable"]:
            continue

        key = (description["classid"], description["instanceid"])

        if key not in description_lookup:
            description_lookup[key] = description

    for asset in inventory["assets"]:
        description = description_lookup.get((asset["classid"], asset["instanceid"]))

        if not description:
            continue

        if add_skus:
            mapped_inventory.append({"sku": get_sku(description)} | asset | description)
        else:
            mapped_inventory.append(asset | description)

    return mapped_inventory


def is_sku_in_inventory(sku: str, mapped_inventory: list[SKUItem]) -> bool:
    return any(i == sku for i in yield_sku(mapped_inventory))


def get_item_in_inventory(sku: str, mapped_inventory: list[SKUItem]) -> dict | None:
    for item in mapped_inventory:
        if item["sku"] == sku:
            return item


def get_last_item_in_inventory(sku: str, mapped_inventory: list[SKUItem]) -> dict | None:
    return get_item_in_inventory(sku, list(reversed(mapped_inventory)))


def get_inventory_stock(mapped_inventory: list[SKUItem]) -> dict[str, int]:
    stock = {}

    for sku in yield_sku(mapped_inventory):
        if sku in stock:
            stock[sku] += 1
        else:
            stock[sku] = 1

    return stock


def get_stock(sku: str, mapped_inventory: list[SKUItem]) -> int:
    return get_inventory_stock(mapped_inventory).get(sku, 0)


def get_keys_and_scrap_in_inventory(mapped_inventory: list[SKUItem]) -> tuple[int, int]:
    keys, scrap = 0, 0

    for sku in yield_sku(mapped_inventory):
        if is_key(sku):
            keys += 1

        if is_metal(sku):
            scrap += get_metal(sku)

    return (keys, scrap)
