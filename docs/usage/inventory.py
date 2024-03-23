from tf2_utils import Inventory, map_inventory

# Create an inventory object
inventory = Inventory("steamsupply", "API KEY")
# steamcommunity, steamsupply and steamapis is supported

# Get the inventory of a user
user_inventory = inventory.fetch("76561198828172881")

# Get the inventory of a user with a different appid
user_inventory = inventory.fetch("76561198253325712", appid=730)

# Map the inventory to a dictionary matching instanceid and classids
mapped_inventory = map_inventory(user_inventory, add_skus=True)
# if add_skus is True, the dictionary will additionaly contain the SKU of the item

print(mapped_inventory)
