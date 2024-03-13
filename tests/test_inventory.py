from src.tf2_utils.utils import read_json_file
from src.tf2_utils import map_inventory

from unittest import TestCase

INVENTORY = read_json_file("./tests/json/bot_inventory.json")


class TestInventory(TestCase):
    def setUp(cls) -> None:
        cls.inventory = map_inventory(INVENTORY, True)

    def test_inventory(self):
        self.assertEqual(500, len(self.inventory))
