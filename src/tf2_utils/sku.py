from .items import Item

from .schema import ITEM_QUALITIES, EFFECTS

from tf2_sku import to_sku


def get_sku_properties(item_description: dict) -> dict:
    item = Item(item_description)

    quality = ITEM_QUALITIES[item.get_quality()]
    effect = item.get_effect()

    sku_properties = {
        "defindex": item.get_defindex(),
        "quality": quality,
        "craftable": item.is_craftable(),
        "australium": item.is_australium(),
    }

    if effect:
        sku_properties["effect"] = EFFECTS[effect]

    # e.g. strange unusual
    if quality != 11:
        sku_properties["strange"] = item.is_strange()

    # TODO: add rest

    return sku_properties

    # to_sku(
    #     {
    #         "defindex": 199,
    #         "quality": 5,
    #         "effect": 702,
    #         "australium": False,
    #         "craftable": True,
    #         "wear": 3,
    #         "skin": 292,
    #         "strange": True,
    #         "killstreak_tier": 3,
    #         "target_defindex": -1,
    #         "festivized": False,
    #         "craft_number": -1,
    #         "crate_number": -1,
    #         "output_defindex": -1,
    #         "output_quality": -1,
    #     }
    # )


def get_sku(item: dict) -> str:
    properties = get_sku_properties(item)
    return to_sku(properties)
