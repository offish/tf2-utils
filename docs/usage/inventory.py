from tf2_utils import Inventory, map_inventory

# Create an inventory object
provider = Inventory("steamsupply", "API KEY")
# steamcommunity, steamsupply, steamapis and custom are supported

# Initialize the inventory object with a custom provider
provider = Inventory("http://localhost:8000", "API KEY")
# requests are sent to {url}/inventory/{steam_id}/{app_id}/{context_id}?api_key=apikey
# or {url}/inventory/{steam_id}/{app_id}/{context_id} if no api_key is provided

# Use steamapis as a provider
provider = Inventory("steamapis", "API KEY")

# Use the default steamcommunity provider
provider = Inventory("steamcommunity")
# or
provider = Inventory()  # (the same as above)
# using steamcommunity will not require an API key and fetches 5000 items at once

# Get the inventory of a user
user_inventory = provider.fetch("76561198828172881")

# Get the inventory of a user with a different appid
user_inventory = provider.fetch("76561198253325712", appid=730)

# Map the inventory to a dictionary matching instanceid and classids
mapped_inventory = map_inventory(user_inventory, add_skus=True)
# if add_skus is True, the dictionary will additionaly contain the SKU of the item

print(mapped_inventory)
