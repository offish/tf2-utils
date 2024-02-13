from src.tf2_utils import (
    account_id_to_steam_id,
    steam_id_to_account_id,
    to_scrap,
    to_refined,
    refinedify,
    get_account_id_from_trade_url,
    get_steam_id_from_trade_url,
    get_token_from_trade_url,
)

from unittest import TestCase

STEAM_ID = "76561198253325712"
ACCOUNT_ID = "293059984"


class TestUtils(TestCase):
    def test_steam_id(self):
        self.assertEqual(STEAM_ID, account_id_to_steam_id(ACCOUNT_ID))
        self.assertEqual(ACCOUNT_ID, steam_id_to_account_id(STEAM_ID))
        self.assertEqual(STEAM_ID, account_id_to_steam_id(int(ACCOUNT_ID)))
        self.assertEqual(ACCOUNT_ID, steam_id_to_account_id(int(STEAM_ID)))

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

    def test_trade_url(self):
        trade_url = "https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR"  # noqa

        self.assertEqual(ACCOUNT_ID, get_account_id_from_trade_url(trade_url))
        self.assertEqual(STEAM_ID, get_steam_id_from_trade_url(trade_url))
        self.assertEqual("0-l_idZR", get_token_from_trade_url(trade_url))
