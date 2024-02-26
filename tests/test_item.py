from src.tf2_utils.utils import read_json_file
from src.tf2_utils import Item, get_sku

from unittest import TestCase

file_path = "./tests/json/{}.json"


def get_item(file_name: str) -> Item:
    return Item(read_json_file(file_path.format(file_name)))


CRUSADERS_CROSSBOW = get_item("crusaders_crossbow")
UNCRAFTABLE_HAT = get_item("uncraftable_hat")
HONG_KONG_CONE = get_item("hong_kong_cone")
SPELLED_ITEM = get_item("spelled_item")
PAINTED_HAT = get_item("painted_hat")
ELLIS_CAP = get_item("ellis_cap")


class TestUtils(TestCase):
    def test_craft_hat(self):
        is_craft_hat = ELLIS_CAP.is_craft_hat()
        is_special = ELLIS_CAP.is_special()
        is_painted = ELLIS_CAP.is_painted()

        self.assertTrue(is_craft_hat)
        self.assertFalse(is_special)
        self.assertFalse(is_painted)

    def test_uncraftable_hat(self):
        is_craftable = UNCRAFTABLE_HAT.is_craftable()
        is_craft_hat = UNCRAFTABLE_HAT.is_craft_hat()
        is_uncraftable = UNCRAFTABLE_HAT.is_uncraftable()

        self.assertFalse(is_craftable)
        self.assertFalse(is_craft_hat)
        self.assertTrue(is_uncraftable)

    def test_painted(self):
        is_special = PAINTED_HAT.is_special()
        is_painted = PAINTED_HAT.is_painted()
        paint = PAINTED_HAT.get_paint()
        is_craft_hat = PAINTED_HAT.is_craft_hat()

        self.assertTrue(is_special)
        self.assertTrue(is_painted)
        self.assertEqual("Australium Gold", paint)
        self.assertTrue(is_craft_hat)

    def test_spell(self):
        is_special = SPELLED_ITEM.is_special()
        has_spell = SPELLED_ITEM.has_spell()
        is_strange = SPELLED_ITEM.is_strange()
        # spell=SPELLED_ITEM.get_spell()

        self.assertTrue(is_special)
        self.assertTrue(has_spell)
        self.assertTrue(is_strange)
        # self.assertEqual("Exorcism", spell)

    def test_unusual(self):
        is_unusual = HONG_KONG_CONE.is_unusual()
        effect = HONG_KONG_CONE.get_effect()
        paint = HONG_KONG_CONE.get_paint()
        is_craft_hat = HONG_KONG_CONE.is_craft_hat()
        strange_in_name = HONG_KONG_CONE.has_strange_in_name()

        self.assertTrue(is_unusual)
        self.assertEqual("Neutron Star", effect)
        self.assertEqual("An Extraordinary Abundance of Tinge", paint)
        self.assertFalse(is_craft_hat)
        self.assertTrue(strange_in_name)

    def test_sku_from_item_class(self):
        sku = get_sku(ELLIS_CAP)

        self.assertEqual("263;6", sku)
