from src.tf2_utils import (
    account_id_to_steam_id,
    get_account_id_from_trade_url,
    get_steam_id_from_trade_url,
    get_token_from_trade_url,
    refinedify,
    steam_id_to_account_id,
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
