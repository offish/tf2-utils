from src.tf2_utils import Item, get_sku, get_sku_properties
from src.tf2_utils.utils import read_json_file

from unittest import TestCase

file_path = "./tests/json/{}.json"

CRUSADERS_CROSSBOW = read_json_file(file_path.format("crusaders_crossbow"))
HONG_KONG_CONE = read_json_file(file_path.format("hong_kong_cone"))
ELLIS_CAP = read_json_file(file_path.format("ellis_cap"))


class TestUtils(TestCase):
    def test_ellis_cap_sku(self):
        sku = get_sku(ELLIS_CAP)

        # https://marketplace.tf/items/tf2/263;6
        self.assertEqual("263;6", sku)

    def test_ellis_cap_sku_properties(self):
        sku = get_sku_properties(ELLIS_CAP)

        self.assertEqual(
            {
                "defindex": 263,
                "quality": 6,
                "australium": False,
                "craftable": True,
                "wear": -1,
                "killstreak_tier": -1,
                "festivized": False,
                "strange": False,
            },
            sku,
        )

    def test_ellis_cap_properties(self):
        item = Item(ELLIS_CAP)
        is_craft_hat = item.is_craft_hat()

        self.assertEqual(True, is_craft_hat)

    def test_crusaders_crossbow_sku(self):
        sku = get_sku(CRUSADERS_CROSSBOW)

        # https://marketplace.tf/items/tf2/305;11;kt-3;festive
        self.assertEqual("305;11;kt-3;festive", sku)

    def test_strange_unusual_hong_kong_cone(self):
        sku = get_sku(HONG_KONG_CONE)

        # https://marketplace.tf/items/tf2/30177;5;u107;strange
        self.assertEqual("30177;5;u107;strange", sku)
