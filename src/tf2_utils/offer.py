import enum

from .utils import account_id_to_steam_id


class TradeOfferState(enum.IntEnum):
    Invalid = 1
    Active = 2
    Accepted = 3
    Countered = 4
    Expired = 5
    Canceled = 6
    Declined = 7
    InvalidItems = 8
    ConfirmationNeed = 9
    CanceledBySecondaryFactor = 10
    StateInEscrow = 11


class Offer:
    def __init__(self, offer: dict) -> None:
        self.offer = offer
        self.state = offer["trade_offer_state"]

    def get_state(self) -> str:
        return TradeOfferState(self.state).name

    def has_state(self, state: int) -> bool:
        return self.state == state

    def is_active(self) -> bool:
        return self.has_state(2)

    def is_accepted(self) -> bool:
        return self.has_state(3)

    def is_declined(self) -> bool:
        return self.has_state(7)

    def has_trade_hold(self) -> bool:
        return self.offer["escrow_end_date"] != 0

    def is_our_offer(self) -> bool:
        return self.offer["is_our_offer"]

    def is_gift(self) -> bool:
        return self.offer.get("items_to_receive") and not self.offer.get(
            "items_to_give"
        )

    def is_scam(self) -> bool:
        return self.offer.get("items_to_give") and not self.offer.get(
            "items_to_receive"
        )

    def is_two_sided(self) -> bool:
        if self.offer.get("items_to_receive") and self.offer.get("items_to_give"):
            return True

        return False

    def is_one_sided(self) -> bool:
        return not self.is_two_sided()

    def get_partner(self) -> str:
        return account_id_to_steam_id(self.offer["accountid_other"])
