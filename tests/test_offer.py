from src.tf2_utils.utils import read_json_file
from src.tf2_utils import Offer

from unittest import TestCase

OFFER = read_json_file("./tests/json/offer.json")

offer = Offer(OFFER)


class TestUtils(TestCase):
    def test_offer_state(self):
        self.assertFalse(offer.is_active())
        self.assertFalse(offer.is_declined())
        self.assertTrue(offer.is_accepted())

    def test_offer_sides(self):
        self.assertFalse(offer.is_our_offer())
        self.assertFalse(offer.is_scam())
        self.assertFalse(offer.is_gift())
        self.assertTrue(offer.is_two_sided())

    def test_offer_partner(self):
        self.assertFalse(offer.has_trade_hold())
        self.assertEqual("76561198253325712", offer.get_partner())
