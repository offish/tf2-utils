from src.tf2_utils.utils import read_json_file
from src.tf2_utils import (
    get_sku,
    get_sku_properties,
    sku_to_defindex,
    sku_to_quality,
    sku_is_uncraftable,
    is_sku,
    sku_to_color,
    is_pure,
    is_metal,
    get_metal,
)

from unittest import TestCase

file_path = "./tests/json/{}.json"


def get_item_dict(file_name: str) -> dict:
    return read_json_file(file_path.format(file_name))


CRUSADERS_CROSSBOW = get_item_dict("crusaders_crossbow")
UNCRAFTABLE_HAT = get_item_dict("uncraftable_hat")
HONG_KONG_CONE = get_item_dict("hong_kong_cone")
ELLIS_CAP = get_item_dict("ellis_cap")


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

    def test_crusaders_crossbow_sku(self):
        sku = get_sku(CRUSADERS_CROSSBOW)

        # https://marketplace.tf/items/tf2/305;11;kt-3;festive
        self.assertEqual("305;11;kt-3;festive", sku)

    def test_strange_unusual_hong_kong_cone(self):
        sku = get_sku(HONG_KONG_CONE)

        # https://marketplace.tf/items/tf2/30177;5;u107;strange
        self.assertEqual("30177;5;u107;strange", sku)

    def test_uncraftable_hat(self):
        sku = get_sku(UNCRAFTABLE_HAT)

        # https://marketplace.tf/items/tf2/734;6;uncraftable
        self.assertEqual("734;6;uncraftable", sku)

    def test_properties(self):
        sku = "734;6;uncraftable"

        self.assertEqual(734, sku_to_defindex(sku))
        self.assertEqual(6, sku_to_quality(sku))
        self.assertEqual(True, sku_is_uncraftable(sku))

    def test_is_sku(self):
        self.assertTrue(is_sku("734;6;uncraftable"))
        self.assertTrue(is_sku("something;text"))
        self.assertFalse(is_sku("734"))

    def test_is_metal(self):
        self.assertTrue(is_metal("5000;6"))
        self.assertTrue(is_metal("5001;6"))
        self.assertTrue(is_metal("5002;6"))
        self.assertFalse(is_metal("5021;6"))

    def test_is_pure(self):
        self.assertTrue(is_pure("5000;6"))
        self.assertTrue(is_pure("5001;6"))
        self.assertTrue(is_pure("5002;6"))
        self.assertTrue(is_pure("5021;6"))
        self.assertFalse(is_pure("5021;7"))

    def test_get_metal(self):
        self.assertEqual(9, get_metal("5002;6"))
        self.assertEqual(3, get_metal("5001;6"))
        self.assertEqual(1, get_metal("5000;6"))
        self.assertRaises(AssertionError, get_metal, "5021;6")

    def test_sku_to_color(self):
        self.assertEqual("7D6D00", sku_to_color("734;6;uncraftable"))
        self.assertEqual("4D7455", sku_to_color("30469;1"))
        self.assertRaises(AssertionError, sku_to_color, "notsku")
