from .providers.steamcommunity import SteamCommunity
from .providers.steamsupply import SteamSupply
from .providers.steamapis import SteamApis
from .sku import get_sku

import requests


def map_inventory(inventory: dict, add_skus: bool = False) -> list[dict]:
    """Matches classids and instanceids, merges these and
    adds `sku` to each item entry if `add_skus` is enabled"""
    mapped_inventory = []

    for asset in inventory["assets"]:
        for desc in inventory["descriptions"]:
            if (
                asset["classid"] != desc["classid"]
                or asset["instanceid"] != desc["instanceid"]
            ):
                continue

            if add_skus:
                mapped_inventory.append({"sku": get_sku(desc), **asset, **desc})
            else:
                mapped_inventory.append({**asset, **desc})
            break

    return mapped_inventory


class Inventory:
    PROVIDERS = [SteamSupply, SteamApis]

    def __init__(
        self, provider_name: str = "steamcommunity", api_key: str = ""
    ) -> None:
        # set default provider for intellisense
        self.provider = SteamCommunity()

        # default to steam if no api_key is given
        if not api_key:
            return

        if provider_name == "steamcommunity":
            # already set
            return

        # loop through providers create object
        for i in self.PROVIDERS:
            if provider_name.lower() == i.__name__.lower():
                # set the first found provider and then stop
                self.provider = i(api_key)
                break

    def fetch(self, steam_id: str, app_id: int = 440, context_id: int = 2) -> dict:
        url, params = self.provider.get_url_and_params(steam_id, app_id, context_id)
        response = requests.get(url, params=params)

        try:
            return response.json()
        except Exception as e:
            return {"error": str(e)}
