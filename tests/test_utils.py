from src.tf2_utils import account_id_to_steam_id, to_scrap, to_refined, refinedify

from unittest import TestCase


class TestUtils(TestCase):
    def test_steam_id(self):
        steam_id = account_id_to_steam_id("293059984")

        self.assertEqual("76561198253325712", steam_id)

    def test_to_refined(self):
        scrap = 43
        refined = to_refined(scrap)

        self.assertEqual(4.77, refined)

    def test_to_scrap(self):
        refined = 2.44
        scrap = to_scrap(refined)

        self.assertEqual(22, scrap)

    def test_refinedify_up(self):
        wrong_value = 32.53
        refined = refinedify(wrong_value)

        self.assertEqual(32.55, refined)

    def test_refinedify_down(self):
        wrong_value = 12.47
        refined = refinedify(wrong_value)

        self.assertEqual(12.44, refined)
