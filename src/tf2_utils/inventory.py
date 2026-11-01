from collections.abc import Iterable

from tf2_sku import is_key, is_metal

from .exceptions import InvalidInventory
from .sku import get_metal, get_sku


def yield_sku(mapped_inventory: list[dict]) -> Iterable[str]:
    for item in mapped_inventory:
        yield item["sku"]


def map_inventory(inventory: dict, add_skus: bool = False, skip_untradable: bool = False) -> list[dict]:
    mapped_inventory = []

    if "assets" not in inventory:
        raise InvalidInventory("No assets found in inventory")

    if "descriptions" not in inventory:
        raise InvalidInventory("No descriptions found in inventory")

    desc_lookup = {}

    for desc in inventory["descriptions"]:
        if skip_untradable and not desc["tradable"]:
            continue

        key = (desc["classid"], desc["instanceid"])

        if key not in desc_lookup:
            desc_lookup[key] = desc

    for asset in inventory["assets"]:
        desc = desc_lookup.get((asset["classid"], asset["instanceid"]))

        if not desc:
            continue

        if add_skus:
            mapped_inventory.append({"sku": get_sku(desc)} | asset | desc)
        else:
            mapped_inventory.append(asset | desc)

    return mapped_inventory


def is_sku_in_inventory(sku: str, mapped_inventory: list[dict]) -> bool:
    return any(i == sku for i in yield_sku(mapped_inventory))


def get_item_in_inventory(sku: str, mapped_inventory: list[dict]) -> dict | None:
    for item in mapped_inventory:
        if item["sku"] == sku:
            return item


def get_last_item_in_inventory(sku: str, mapped_inventory: list[dict]) -> dict | None:
    return get_item_in_inventory(sku, list(reversed(mapped_inventory)))


def get_inventory_stock(mapped_inventory: list[dict]) -> dict[str, int]:
    stock = {}

    for sku in yield_sku(mapped_inventory):
        if sku in stock:
            stock[sku] += 1
        else:
            stock[sku] = 1

    return stock


def get_stock(sku: str, mapped_inventory: list[dict]) -> int:
    return get_inventory_stock(mapped_inventory).get(sku, 0)


def get_keys_and_scrap_in_inventory(mapped_inventory: list[dict]) -> tuple[int, int]:
    keys = 0
    scrap = 0

    for sku in yield_sku(mapped_inventory):
        if is_key(sku):
            keys += 1

        if is_metal(sku):
            scrap += get_metal(sku)

    return (keys, scrap)
