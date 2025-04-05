import re

from tf2_data import COLORS, EFFECTS, QUALITIES
from tf2_sku import to_sku

from .item import Item

__all__ = [
    "get_sku",
    "get_sku_properties",
    "is_sku",
    "is_key",
    "is_metal",
    "is_pure",
    "get_metal",
    "get_properties",
    "get_property",
    "get_property_by_key",
    "sku_to_defindex",
    "sku_to_quality",
    "sku_to_quality_name",
    "sku_to_color",
    "sku_is_uncraftable",
    "sku_is_craftable",
    "strange_in_sku",
    "australium_in_sku",
    "festive_in_sku",
    "get_sku_killstreak",
    "get_killstreak_name_from_sku",
    "get_sku_effect",
    "get_effect_name_from_sku",
]


def get_sku_properties(item: Item | dict) -> dict:
    if isinstance(item, dict):
        item = Item(item)

    quality = item.get_quality_id()
    effect = item.get_effect()

    sku_properties = {
        "defindex": item.get_defindex(),
        "quality": quality,
        "australium": item.is_australium(),
        "craftable": item.is_craftable(),
        "wear": item.get_exterior_id(),
        "killstreak_tier": item.get_killstreak_id(),
        "festivized": item.is_festivized(),
    }
    # "skin": "pk{}",
    # "target_defindex": "td-{}",
    # "craft_number": "n{}",
    # "crate_number": "c{}",
    # "output_defindex": "od-{}",
    # "output_quality": "oq-{}",

    if effect:
        sku_properties["effect"] = EFFECTS[effect]

    # e.g. strange unusual
    if quality != 11:
        sku_properties["strange"] = item.has_strange_in_name()

    return sku_properties


def is_sku(item: str) -> bool:
    return item.find(";") != -1


def is_key(sku: str) -> bool:
    return sku == "5021;6"


def is_metal(sku: str) -> bool:
    return sku in ["5000;6", "5001;6", "5002;6"]


def is_pure(sku: str) -> bool:
    return is_metal(sku) or is_key(sku)


def get_metal(sku: str) -> int:
    assert is_metal(sku), f"sku {sku} is not metal"

    if sku == "5002;6":
        return 9

    if sku == "5001;6":
        return 3

    if sku == "5000;6":
        return 1


def get_properties(sku: str) -> list[str]:
    assert is_sku(sku), f"sku {sku} is not valid"

    return sku.split(";")


def get_property(sku: str, index: int) -> str:
    return get_properties(sku)[index]


def get_property_by_key(sku: str, key: str) -> str | None:
    for p in get_properties(sku):
        match = re.search(key + r"(\d+)", p)

        if match:
            return match.group(1)


def sku_to_defindex(sku: str) -> int:
    return int(get_property(sku, 0))


def sku_to_quality(sku: str) -> int:
    return int(get_property(sku, 1))


def sku_to_quality_name(sku: str) -> str:
    return QUALITIES[str(sku_to_quality(sku))]


def sku_to_color(sku: str) -> str:
    return COLORS[str(sku_to_quality(sku))]


def sku_is_uncraftable(sku: str) -> bool:
    return ";uncraftable" in sku


def sku_is_craftable(sku: str) -> bool:
    return not sku_is_uncraftable(sku)


def strange_in_sku(sku: str) -> bool:
    return ";strange" in sku


def australium_in_sku(sku: str) -> bool:
    return ";australium" in sku


def festive_in_sku(sku: str) -> bool:
    return ";festive" in sku


def get_sku_killstreak(sku: str) -> int:
    value = get_property_by_key(sku, "kt-")

    if value is None:
        return -1

    return int(value.replace("kt-", ""))


def get_killstreak_name_from_sku(sku: str) -> str:
    tier = get_sku_killstreak(sku)
    name = ""

    if tier == 1:
        name = "Basic Killstreak "

    if tier == 2:
        name = "Specialized "

    if tier == 3:
        name = "Professional "

    return name


def get_sku_effect(sku: str) -> int:
    value = get_property_by_key(sku, "u")

    if value is None:
        return -1

    return int(value.replace("u", ""))


def get_effect_name_from_sku(sku: str) -> str:
    effect = get_sku_effect(sku)
    name = ""

    if effect != -1:
        name = EFFECTS[str(effect)] + " "

    return name


def get_sku(item: Item | dict) -> str:
    if isinstance(item, dict):
        item = Item(item)

    properties = get_sku_properties(item)
    return to_sku(properties)
