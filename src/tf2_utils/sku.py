from tf2_data import COLORS, EFFECTS, QUALITIES
from tf2_sku import get_effect, get_killstreak, get_quality, is_metal, to_sku

from .item import Item

__all__ = [
    "get_sku",
    "get_sku_properties",
    "get_metal",
    "sku_to_quality_name",
    "sku_to_color",
    "get_killstreak_name_from_sku",
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
    # "crate_number": "c{}",
    # "output_defindex": "od-{}",
    # "output_quality": "oq-{}",
    # "craft_number": "n{}",

    if effect:
        sku_properties["effect"] = EFFECTS[effect]

    # e.g. strange unusual
    if quality != 11:
        sku_properties["strange"] = item.has_strange_in_name()

    return sku_properties


def get_metal(sku: str) -> int:
    assert is_metal(sku), f"sku {sku} is not metal"

    if sku == "5002;6":
        return 9

    if sku == "5001;6":
        return 3

    if sku == "5000;6":
        return 1


def sku_to_quality_name(sku: str) -> str:
    return QUALITIES[str(get_quality(sku))]


def sku_to_color(sku: str) -> str:
    return COLORS[str(get_quality(sku))]


def get_killstreak_name_from_sku(sku: str) -> str:
    tier = get_killstreak(sku)
    name = ""

    if tier == 1:
        name = "Basic Killstreak "

    if tier == 2:
        name = "Specialized "

    if tier == 3:
        name = "Professional "

    return name


def get_effect_name_from_sku(sku: str) -> str:
    effect = get_effect(sku)
    name = ""

    if effect != -1:
        name = EFFECTS[str(effect)] + " "

    return name


def get_sku(item: Item | dict) -> str:
    if isinstance(item, dict):
        item = Item(item)

    properties = get_sku_properties(item)
    return to_sku(properties)
