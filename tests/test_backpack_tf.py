from unittest import TestCase

from .config import BACKPACK_TF_TOKEN
from src.tf2_utils import BackpackTF, Currencies


class TestBackpackTF(TestCase):
    def setUp(cls) -> None:
        cls.bptf = BackpackTF(BACKPACK_TF_TOKEN, "76561198253325712")

    def test_currencies(self):
        self.assertEqual(Currencies(1, 1.5).__dict__, {"keys": 1, "metal": 1.5})
        self.assertEqual(Currencies().__dict__, {"keys": 0, "metal": 0.0})
        self.assertEqual(
            Currencies(**{"metal": 10.55}).__dict__, {"keys": 0, "metal": 10.55}
        )

    def test_construct_listing_item(self):
        self.assertDictEqual(
            self.bptf._construct_listing_item("263;6"),
            {
                "baseName": "Ellis' Cap",
                "craftable": True,
                "quality": {"id": 6},
                "tradable": True,
            },
        )

    def test_construct_listing(self):
        self.assertDictEqual(
            self.bptf._construct_listing(
                "263;6",
                "sell",
                {"keys": 1, "metal": 1.55},
                "my description",
                13201231975,
            ),
            {
                "item": {
                    "baseName": "Ellis' Cap",
                    "craftable": True,
                    "quality": {"id": 6},
                    "tradable": True,
                },
                "currencies": {"keys": 1, "metal": 1.55},
                "details": "my description",
                "id": 13201231975,
            },
        )
        self.assertDictEqual(
            self.bptf._construct_listing(
                "263;6", "buy", {"keys": 1, "metal": 1.55}, "my description"
            ),
            {
                "item": {
                    "baseName": "Ellis' Cap",
                    "craftable": True,
                    "quality": {"id": 6},
                    "tradable": True,
                },
                "currencies": {"keys": 1, "metal": 1.55},
                "details": "my description",
            },
        )

    def test_hash_name(self):
        self.assertEqual(
            self.bptf._get_sku_item_hash("5021;6"), "d9f847ff5dfcf78576a9fca04cbf6c07"
        )
        self.assertEqual(
            self.bptf._get_sku_item_hash("30397;6"), "8010db121d19610e9bcbac47432bd78c"
        )
        self.assertEqual(
            self.bptf._get_item_hash("The Bruiser's Bandanna"),
            "8010db121d19610e9bcbac47432bd78c",
        )
