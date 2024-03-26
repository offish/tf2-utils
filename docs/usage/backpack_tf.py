from tf2_utils import BackpackTF

bptf = BackpackTF(
    "token",
    "steam_id",
    "api key not needed as of now",
    "superbot5000's user agent message",
)

# will add the lightning icon and indicate that the user is a bot
bptf.register_user_agent()

listing = bptf.create_listing(
    "5021;6", "buy", {"metal": 62.11}, "buying keys for listed price :)"
)

print(listing)

asset_id = 11543535227
listing = bptf.create_listing(
    "30745;6",
    "sell",
    {"keys": 1, "metal": 2.11},
    "selling my Siberian Sweater as i dont want it anymore",
    11543535227,
)

print(listing)

bptf.delete_listing_by_asset_id(11543535227)  # sell
bptf.delete_listing_by_sku("5021;6")  # buy
# or
bptf.delete_all_listings()
