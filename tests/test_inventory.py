from src.tf2_utils import map_inventory
from src.tf2_utils.utils import read_json_file

INVENTORY = read_json_file("./tests/json/bot_inventory.json")
inventory = map_inventory(INVENTORY, True)


def test_inventory() -> None:
    assert 500 == len(inventory)

    for item in inventory:
        assert "sku" in item
