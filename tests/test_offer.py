from src.tf2_utils import Offer
from src.tf2_utils.utils import read_json_file

OFFER = read_json_file("./tests/json/offer.json")

offer = Offer(OFFER)


def test_offer_state() -> None:
    assert not offer.is_active()
    assert not offer.is_declined()
    assert offer.is_accepted()


def test_offer_sides() -> None:
    assert not offer.is_our_offer()
    assert not offer.is_scam()
    assert not offer.is_gift()
    assert offer.is_two_sided()


def test_offer_partner() -> None:
    assert not offer.has_trade_hold()
    assert offer.get_partner() == "76561198253325712"
