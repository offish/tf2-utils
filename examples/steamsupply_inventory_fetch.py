from tf2_utils import Inventory, map_inventory

provider = Inventory("steamsupply", "9st947vs0qmgfpeqde1gj92l0oqmhysm")

user_inventory = provider.fetch("76561198253325712")
inventory = map_inventory(user_inventory, add_skus=True)

print(inventory)
