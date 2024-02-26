from .item import Item

from tf2_data import EFFECTS, COLORS
from tf2_sku import to_sku


def get_sku_properties(item: Item | dict) -> dict:
    if isinstance(item, dict):
        item = Item(item)

    quality = item.get_quality_id()
    effect = item.get_effect()

    # TODO: add rest
    sku_properties = {
        "defindex": item.get_defindex(),
        "quality": quality,
        "australium": item.is_australium(),
        "craftable": item.is_craftable(),
        "wear": item.get_exterior_id(),
        "killstreak_tier": item.get_killstreak_id(),
        "festivized": item.is_festivized(),
        #
        # "effect": "u{}",
        # "australium": "australium",
        # "craftable": "uncraftable",
        # "wear": "w{}",
        # "skin": "pk{}",
        # "strange": "strange",
        # "killstreak_tier": "kt-{}",
        # "target_defindex": "td-{}",
        # "festivized": "festive",
        # "craft_number": "n{}",
        # "crate_number": "c{}",
        # "output_defindex": "od-{}",
        # "output_quality": "oq-{}",
    }

    if effect:
        sku_properties["effect"] = EFFECTS[effect]

    # e.g. strange unusual
    if quality != 11:
        sku_properties["strange"] = item.has_strange_in_name()

    return sku_properties


def is_sku(item: str) -> bool:
    return item.find(";") != -1


def is_pure(sku: str) -> bool:
    return sku in ["5000;6", "5001;6", "5002;6", "5021;6"]


def is_metal(sku: str) -> bool:
    return sku in ["5000;6", "5001;6", "5002;6"]


def get_metal(sku: str) -> int:
    assert is_metal(sku), f"sku {sku} is not metal"

    match sku:
        # refined
        case "5002;6":
            return 9

        # reclaimed
        case "5001;6":
            return 3

        # scrap
        case "5000;6":
            return 1


def get_property(sku: str, index: int) -> str:
    assert is_sku(sku), f"sku {sku} is not valid"

    return sku.split(";")[index]


def sku_to_defindex(sku: str) -> int:
    return int(get_property(sku, 0))


def sku_to_quality(sku: str) -> int:
    return int(get_property(sku, 1))


def sku_to_color(sku: str) -> str:
    return COLORS[str(sku_to_quality(sku))]


def sku_is_uncraftable(sku: str) -> bool:
    return sku.find(";uncraftable") != -1


def get_sku(item: Item | dict) -> str:
    if isinstance(item, dict):
        item = Item(item)

    properties = get_sku_properties(item)
    return to_sku(properties)
