from .items import Item

from .schema import ITEM_QUALITIES, EFFECTS

from tf2_sku import to_sku


def get_sku_properties(item_description: dict) -> dict:
    item = Item(item_description)

    effect = item.get_effect()
    quality = ITEM_QUALITIES[item.get_quality()]

    return {
        "defindex": item.get_defindex(),
        "quality": quality,
        "effect": EFFECTS[effect] if effect else -1,
        "craftable": item.is_craftable(),
        "australium": item.is_australium(),
        "strange": item.is_strange() if quality != 11 else False
        # TODO: add rest...
    }

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
    #         "paint": -1,
    #     }
    # )


def get_sku(item: dict) -> str:
    properties = get_sku_properties(item)
    return to_sku(properties)
