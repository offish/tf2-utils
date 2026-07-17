import pytest

from src.tf2_utils import (
    account_id_to_steam_id,
    get_account_id_from_trade_url,
    get_steam_id_from_trade_url,
    get_token_from_trade_url,
    is_half_scrap_price,
    refinedify,
    steam_id_to_account_id,
    swap_intent,
    to_refined,
    to_scrap,
)


def test_steam_id(steam_id: str, account_id: str) -> None:
    assert account_id_to_steam_id(account_id) == steam_id
    assert steam_id_to_account_id(steam_id) == account_id
    assert account_id_to_steam_id(int(account_id)) == steam_id
    assert steam_id_to_account_id(int(steam_id)) == account_id


def test_to_refined() -> None:
    assert to_refined(43) == 4.77


def test_to_scrap() -> None:
    assert to_scrap(2.44) == 22


def test_refinedify() -> None:
    assert refinedify(32.53) == 32.55
    assert refinedify(12.47) == 12.44


def test_trade_url(steam_id: str, account_id: str) -> None:
    trade_url = (
        "https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR"
    )

    assert get_account_id_from_trade_url(trade_url) == account_id
    assert get_steam_id_from_trade_url(trade_url) == steam_id
    assert get_token_from_trade_url(trade_url) == "0-l_idZR"


def test_swap_intent() -> None:
    assert swap_intent("buy") == "sell"
    assert swap_intent("BUY") == "sell"
    assert swap_intent("sell") == "buy"
    assert swap_intent("Sell") == "buy"

    with pytest.raises(AssertionError):
        swap_intent("asdf")


def test_half_scrap_price() -> None:
    assert is_half_scrap_price(0.05)
    assert is_half_scrap_price(0.16)
    assert is_half_scrap_price(0.27)
    assert is_half_scrap_price(0.38)
    assert is_half_scrap_price(0.5)
    assert is_half_scrap_price(0.61)
    assert is_half_scrap_price(0.72)
    assert is_half_scrap_price(0.83)
    assert is_half_scrap_price(0.94)
    assert not is_half_scrap_price(0.11)
    assert not is_half_scrap_price(0.22)
    assert not is_half_scrap_price(0.33)
    assert not is_half_scrap_price(0.44)
    assert not is_half_scrap_price(0.55)
    assert not is_half_scrap_price(0.66)
    assert not is_half_scrap_price(0.77)
    assert not is_half_scrap_price(0.88)
    assert not is_half_scrap_price(1)
    assert not is_half_scrap_price(1.11)
