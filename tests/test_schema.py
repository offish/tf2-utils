from src.tf2_utils import SchemaItemsUtils

from unittest import TestCase


schema_items = SchemaItemsUtils()  # uses local files by default


class TestUtils(TestCase):
    def test_map_defindex_names(self):
        response = schema_items.map_defindex_name()
        self.assertNotEqual({}, response)

    def test_name_to_sku_tod(self):
        sku = schema_items.name_to_sku("Uncraftable Tour of Duty Ticket")
        self.assertEqual("725;6;uncraftable", sku)

    def test_name_to_sku_key(self):
        sku = schema_items.name_to_sku("Mann Co. Supply Crate Key")
        self.assertEqual("5021;6", sku)

    def test_name_to_sku_name_tag(self):
        sku = schema_items.name_to_sku("Name Tag")
        self.assertEqual("5020;6", sku)

    def test_name_to_sku_pure(self):
        ref = schema_items.name_to_sku("Refined Metal")
        rec = schema_items.name_to_sku("Reclaimed Metal")
        scrap = schema_items.name_to_sku("Scrap Metal")

        self.assertEqual("5002;6", ref)
        self.assertEqual("5001;6", rec)
        self.assertEqual("5000;6", scrap)

    def test_name_to_sku_non_existing(self):
        # this item does not exist
        item_name = "Non-Craftable Strange Team Captain"
        sku = schema_items.name_to_sku(item_name)
        defindex = schema_items.name_to_defindex(item_name)

        self.assertEqual("378;11;uncraftable", sku)
        self.assertEqual(-1, defindex)

    def test_name_to_sku_qualities(self):
        unique = schema_items.name_to_sku("Team Captain")
        genuine = schema_items.name_to_sku("Genuine Team Captain")
        haunted = schema_items.name_to_sku("Haunted Team Captain")
        strange = schema_items.name_to_sku("Strange Team Captain")
        vintage = schema_items.name_to_sku("Vintage Team Captain")
        collectors = schema_items.name_to_sku("Collector's Team Captain")

        self.assertEqual("378;1", genuine)
        self.assertEqual("378;3", vintage)
        self.assertEqual("378;6", unique)
        self.assertEqual("378;11", strange)
        self.assertEqual("378;13", haunted)
        self.assertEqual("378;14", collectors)

    def test_defindex_to_name(self):
        self.assertEqual("Tour of Duty Ticket", schema_items.defindex_to_name(725))
        self.assertEqual(
            "Mann Co. Supply Crate Key", schema_items.defindex_to_name(5021)
        )
        self.assertEqual("Random Craft Hat", schema_items.defindex_to_name(-100))
        self.assertEqual("Random Craft Weapon", schema_items.defindex_to_name(-50))
        self.assertEqual("Scrap Metal", schema_items.defindex_to_name(5000))
        self.assertEqual("Reclaimed Metal", schema_items.defindex_to_name(5001))
        self.assertEqual("Refined Metal", schema_items.defindex_to_name(5002))

    def test_sku_to_name_tod(self):
        name = schema_items.sku_to_name("725;6;uncraftable")
        self.assertEqual("Tour of Duty Ticket", name)

    def test_sku_to_name_key(self):
        name = schema_items.sku_to_name("5021;6")
        self.assertEqual("Mann Co. Supply Crate Key", name)

    def test_image_equal(self):
        ellis_cap = schema_items.defindex_to_image_url(263)
        random_craft_hat = schema_items.sku_to_image_url("-100;6")
        self.assertEqual(ellis_cap, random_craft_hat)
