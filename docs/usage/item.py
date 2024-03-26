from tf2_utils import Item

# A dictionary of item data from inventory or offer
item_dict = {
    "appid": 440,
    "classid": "313",
    "instanceid": "11040552",
    # and so on...
}

# Create an item object
item = Item(item_dict)

item.get_defindex()  # 263
item.is_craft_hat()  # True
item.is_uncraftable()  # False
item.get_paint()  # Australium Gold
item.is_unusual()  # False
item.is_unusual_cosmetic()  # False
item.get_effect()  # ""
# etc.
