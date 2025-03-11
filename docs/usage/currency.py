from tf2_utils import CurrencyExchange, Inventory, map_inventory

inventory_provider = Inventory("steamcommunity")

# Get our inventory of a user
our_inventory = map_inventory(inventory_provider.fetch("76561198253325712"))

# Get their inventory
their_inventory = map_inventory(inventory_provider.fetch("76561198828172881"))

item_price = 13  # in scrap, so this is 1.44 ref
intent = "sell"  # or "buy". This is the intent related to us,
# so if we have the item on our side we are selling.

key_price = 64 * 9  # value of key in scrap, IMPORTANT that this value is
# up-to-date and not ridiculously priced

item_is_not_pure = True  # only False if the trade is a metal or key trade only.
# no other items such as hats, taunts, etc.

# Create a currency exchange object
currency = CurrencyExchange(
    their_inventory, our_inventory, intent, item_price, key_price, item_is_not_pure
)

currency.calculate()

if not currency.is_possible:
    print("Trade is not possible")
    # either no combination worked, or someone did not have enough pure

else:
    their_items, our_items = currency.get_currencies()

    print(their_items)
    print(our_items)

    # their_items is a list of item dicts including "assetid"
    # our_items is a list of item dicts including "assetid"
    # see tf2-express' send_offer method for how to use this data with steampy
