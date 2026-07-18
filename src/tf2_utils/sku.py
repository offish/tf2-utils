from tf2_data import COLORS, EFFECTS, QUALITIES
from tf2_sku import get_effect, get_killstreak, get_quality, is_metal, to_sku

from .item import Item


def get_sku_properties(item: Item | dict) -> dict:
    if isinstance(item, dict):
        item = Item(item)

    quality = item.get_quality_id()

    sku_properties = {
        "defindex": item.get_defindex(),
        "quality": quality,
        "effect": item.get_effect_id(),
        "australium": item.is_australium(),
        "craftable": item.is_craftable(),
        "wear": item.get_wear_id(),
        "skin": item.get_skin_id(),
        "killstreak_tier": item.get_killstreak_tier(),
        "sheen": item.get_sheen_id(),
        "killstreaker": item.get_killstreaker_id(),
        "festivized": item.is_festivized(),
        "crate_number": item.get_crate_series(),
    }
    # "target_defindex": "td-{}",
    # "output_defindex": "od-{}",
    # "output_quality": "oq-{}",

    # e.g. strange unusual
    if quality != 11:
        sku_properties["strange"] = item.has_strange_in_name()

    return sku_properties


def get_sku(item: Item | dict) -> str:
    if isinstance(item, dict):
        item = Item(item)

    properties = get_sku_properties(item)
    return to_sku(properties)


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


def get_killstreak_name_from_sku(sku: str) -> str | None:
    match get_killstreak(sku):
        case 1:
            return "Basic Killstreak"
        case 2:
            return "Specialized"
        case 3:
            return "Professional"


def get_effect_name_from_sku(sku: str) -> str | None:
    effect = get_effect(sku)

    if effect == -1:
        return

    return EFFECTS[str(effect)]
