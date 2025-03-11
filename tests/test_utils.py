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

STEAM_ID = "76561198253325712"
ACCOUNT_ID = "293059984"


def test_steam_id() -> None:
    assert STEAM_ID == account_id_to_steam_id(ACCOUNT_ID)
    assert ACCOUNT_ID == steam_id_to_account_id(STEAM_ID)
    assert STEAM_ID == account_id_to_steam_id(int(ACCOUNT_ID))
    assert ACCOUNT_ID == steam_id_to_account_id(int(STEAM_ID))


def test_to_refined() -> None:
    scrap = 43
    refined = to_refined(scrap)

    assert 4.77 == refined


def test_to_scrap() -> None:
    refined = 2.44
    scrap = to_scrap(refined)

    assert 22 == scrap


def test_refinedify_up() -> None:
    wrong_value = 32.53
    refined = refinedify(wrong_value)

    assert 32.55 == refined


def test_refinedify_down() -> None:
    wrong_value = 12.47
    refined = refinedify(wrong_value)

    assert 12.44 == refined


def test_trade_url() -> None:
    trade_url = (
        "https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR"  # noqa
    )

    assert ACCOUNT_ID == get_account_id_from_trade_url(trade_url)
    assert STEAM_ID == get_steam_id_from_trade_url(trade_url)
    assert "0-l_idZR" == get_token_from_trade_url(trade_url)
