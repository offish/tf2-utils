from src.tf2_utils.providers.express_load import ExpressLoad
from src.tf2_utils.providers.steamcommunity import SteamCommunity


def test_steam_community_inventory(steam_id: str) -> None:
    provider = SteamCommunity()
    url, params = provider.get_url_and_params(steam_id, 440, 2)

    assert provider.api_key == ""
    assert url == f"https://steamcommunity.com/inventory/{steam_id}/440/2"
    assert params == {
        "l": "english",
        "count": 5000,
    }
    assert provider.headers == {}


def test_express_load_inventory(express_load_api_key: str, steam_id: str) -> None:
    provider = ExpressLoad(express_load_api_key)
    url, params = provider.get_url_and_params(steam_id, 440, 2)

    assert url == f"https://api.express-load.com/inventory/{steam_id}/440/2"
    assert params == {}
    assert provider.headers == {
        "X-API-Key": express_load_api_key,
        "User-Agent": "tf2-express",
    }
