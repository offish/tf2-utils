import pytest

from src.tf2_utils.providers.express_load import ExpressLoad
from src.tf2_utils.providers.steamcommunity import SteamCommunity


@pytest.mark.parametrize("steam_id", ["76561198253325712"])
def test_steam_community_inventory(steam_id: str) -> None:
    provider = SteamCommunity()
    url, params = provider.get_url_and_params(steam_id, 440, 2)

    assert provider.api_key == ""
    assert url == f"https://steamcommunity.com/inventory/{steam_id}/440/2"
    assert params == {
        "l": "english",
        "count": 2500,
    }
    assert provider.headers["User-Agent"].startswith("Mozilla/5.0 ")
    assert "Chrome/" in provider.headers["User-Agent"]
    assert provider.headers["Referer"] == (
        f"https://steamcommunity.com/profiles/{steam_id}/inventory"
    )


def test_steam_community_api_key() -> None:
    provider = SteamCommunity("api_key")

    assert provider.api_key == "api_key"
    assert provider.headers["User-Agent"] == (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    )


def test_steam_community_headers_are_independent() -> None:
    first = SteamCommunity()
    second = SteamCommunity()
    first.get_url_and_params("76561198253325712", 440, 2)

    assert second.headers["User-Agent"].startswith("Mozilla/5.0 ")
    assert "Referer" not in second.headers


def test_steam_community_referer_tracks_inventory() -> None:
    provider = SteamCommunity()
    for steam_id in ["76561198253325712", "76561198828172881"]:
        url, params = provider.get_url_and_params(steam_id, 730, 2)
        assert url == f"https://steamcommunity.com/inventory/{steam_id}/730/2"
        assert params == {"l": "english", "count": 2500}
        assert provider.headers["Referer"] == (
            f"https://steamcommunity.com/profiles/{steam_id}/inventory"
        )
        assert len(provider.headers) == 2


def test_express_load_inventory(express_load_api_key: str, steam_id: str) -> None:
    provider = ExpressLoad(express_load_api_key)
    url, params = provider.get_url_and_params(steam_id, 440, 2)

    assert url == f"https://api.express-load.com/inventory/{steam_id}/440/2"
    assert params == {}
    assert provider.headers == {
        "X-API-Key": express_load_api_key,
        "User-Agent": "tf2-express",
    }
