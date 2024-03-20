from .item import Item

from tf2_data import EFFECTS, COLORS, QUALITIES
from tf2_sku import to_sku


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
    # TODO: add rest
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


def get_properties(sku: str) -> list[str]:
    assert is_sku(sku), f"sku {sku} is not valid"

    return sku.split(";")


def get_property(sku: str, index: int) -> str:
    return get_sku_properties(sku)[index]


def get_property_by_key(sku: str, key: str) -> str:
    for p in get_properties(sku):
        # so n{} does not match with strange etc.
        if f";{key}" in f";{p}":
            return p

    return ""


def sku_to_defindex(sku: str) -> int:
    return int(get_property(sku, 0))


def sku_to_quality(sku: str) -> int:
    return int(get_property(sku, 1))


def sku_to_quality_name(sku: str) -> str:
    return QUALITIES[str(sku_to_quality(sku))]


def sku_to_color(sku: str) -> str:
    return COLORS[str(sku_to_quality(sku))]


def sku_is_craftable(sku: str) -> bool:
    return ";uncraftable" in sku


def sku_is_uncraftable(sku: str) -> bool:
    return not sku_is_craftable(sku)


def strange_in_sku(sku: str) -> bool:
    return ";strange" in sku


def get_sku_killstreak(sku: str) -> int:
    value = get_property_by_key(sku, "kt-")

    if not value:
        return -1

    return int(value.replace("kt-", ""))


def get_sku_effect(sku: str) -> int:
    value = get_property_by_key(sku, "u")

    if not value:
        return -1

    return int(value.replace("u", ""))


def get_sku(item: Item | dict) -> str:
    if isinstance(item, dict):
        item = Item(item)

    properties = get_sku_properties(item)
    return to_sku(properties)
