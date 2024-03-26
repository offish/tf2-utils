from tf2_utils import (
    Item,
    get_sku,
    is_metal,
    sku_is_uncraftable,
    sku_to_quality,
    get_sku_properties,
)

# A dictionary of item data from inventory or offer
item_dict = {
    "appid": 440,
    "classid": "313",
    "instanceid": "11040552",
    # and so on...
}

get_sku(item_dict)  # 263;6

# or

itm = Item(item_dict)
get_sku(itm)  # 263;6
get_sku_properties(itm)  # {"defindex": 263, "quality": 6, "craftable": True, ...}


sku = "725;6;uncraftable"

sku_is_uncraftable(sku)  # True
is_metal(sku)  # False
sku_to_quality(sku)  # 6
