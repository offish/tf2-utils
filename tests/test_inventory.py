from unittest.mock import Mock, patch

import pytest

from src.tf2_utils import InvalidInventory, map_inventory
from src.tf2_utils.inventory import Inventory
from src.tf2_utils.utils import read_json_file

INVENTORY = read_json_file("./tests/json/bot_inventory.json")
inventory = map_inventory(INVENTORY, True)


def test_inventory() -> None:
    assert 500 == len(inventory)

    for item in inventory:
        assert "sku" in item


def test_raises_error() -> None:
    with pytest.raises(InvalidInventory):
        map_inventory({}, False)


def test_default_inventory_provider() -> None:
    inventory = Inventory()
    assert inventory.provider.__class__.__name__ == "SteamCommunity"
    assert inventory.provider.api_key == ""


def test_steamcommunity_inventory_provider() -> None:
    inventory = Inventory("steamcommunity", "api_key")
    assert inventory.provider.__class__.__name__ == "SteamCommunity"
    assert inventory.provider.api_key == "api_key"


def test_express_load_inventory_provider() -> None:
    inventory = Inventory("expressload", "api_key")
    assert inventory.provider.__class__.__name__ == "ExpressLoad"
    assert inventory.provider.api_key == "api_key"


def test_steamsupply_inventory_provider() -> None:
    inventory = Inventory("steamsupply", "api_key")
    assert inventory.provider.__class__.__name__ == "SteamSupply"
    assert inventory.provider.api_key == "api_key"


def test_custom_inventory_provider() -> None:
    inventory = Inventory("http://example.com", "api_key")
    assert inventory.provider.__class__.__name__ == "Custom"
    assert inventory.provider.api_key == "api_key"


def test_steamapis_inventory_provider() -> None:
    inventory = Inventory("steamapis", "api_key")
    assert inventory.provider.__class__.__name__ == "SteamApis"
    assert inventory.provider.api_key == "api_key"


@pytest.mark.parametrize("app_id,context_id", [(440, 2), (730, 3)])
def test_steamcommunity_inventory_request(app_id, context_id) -> None:
    inventory = Inventory()
    response = Mock()
    response.json.return_value = INVENTORY

    with patch("src.tf2_utils.inventory.requests.get", return_value=response) as get:
        for steam_id in ["76561198253325712", "76561198828172881"]:
            assert inventory.fetch(steam_id, app_id, context_id) is INVENTORY
            get.assert_called_with(
                f"https://steamcommunity.com/inventory/"
                f"{steam_id}/{app_id}/{context_id}",
                params={"l": "english", "count": 2500},
                headers=inventory.provider.headers,
            )
            headers = get.call_args.kwargs["headers"]
            assert headers["Referer"] == (
                f"https://steamcommunity.com/profiles/{steam_id}/inventory"
            )
            assert headers["User-Agent"] == (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/130.0.0.0 Safari/537.36"
            )
            assert "Origin" not in headers


def test_steamcommunity_inventory_fetch(steam_id: str) -> None:
    provider = Inventory("steamcommunity")
    inventory = provider.fetch(steam_id)

    assert "assets" in inventory
    assert "descriptions" in inventory


def test_express_load_inventory_fetch(express_load_api_key: str, steam_id: str) -> None:
    provider = Inventory("expressload", express_load_api_key)
    inventory = provider.fetch(steam_id)

    assert "success" in inventory
    assert "assets" in inventory
    assert "descriptions" in inventory
