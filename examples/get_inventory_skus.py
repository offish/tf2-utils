from tf2_utils import map_inventory
import json

local_inventory = json.loads(open("./example_inventory.json", "r").read())
inventory = map_inventory(local_inventory, add_skus=True)

for item in inventory:
    print(item)
