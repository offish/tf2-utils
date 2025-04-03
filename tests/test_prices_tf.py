import pytest

from src.tf2_utils import PricesTF, UnauthorizedError

prices_tf = PricesTF()


def test_inital() -> None:
    assert prices_tf._access_token == ""
    assert prices_tf._headers == {}

    with pytest.raises(UnauthorizedError):
        prices_tf.get_price("5021;6")

    prices_tf.request_access_token()

    assert prices_tf._access_token != ""
    assert prices_tf._headers != {}


def test_get_price() -> None:
    price = prices_tf.get_price("5021;6")

    assert isinstance(price, dict)
    assert "sku" in price
    assert "buyHalfScrap" in price
    assert "buyKeys" in price
    assert "buyKeyHalfScrap" in price
    assert "sellHalfScrap" in price
    assert "sellKeys" in price
    assert "sellKeyHalfScrap" in price
    assert "createdAt" in price
    assert "updatedAt" in price


def test_formatting_price() -> None:
    item = {
        "sku": "5021;6",
        "buyHalfScrap": 1210,
        "buyKeys": 0,
        "buyKeyHalfScrap": None,
        "sellHalfScrap": 1212,
        "sellKeys": 0,
        "sellKeyHalfScrap": None,
        "createdAt": "2021-10-11T23:05:32.696Z",
        "updatedAt": "2025-04-03T16:36:22.624Z",
    }
    formatted_price = prices_tf.format_price(item)

    assert formatted_price["buy"]["keys"] == 0
    assert formatted_price["buy"]["metal"] == 67.22
    assert formatted_price["sell"]["keys"] == 0
    assert formatted_price["sell"]["metal"] == 67.33


def test_get_prices_till_page() -> None:
    pages = 2
    prices = prices_tf.get_prices_till_page(pages)

    assert len(prices) == pages * 50

    for sku in prices:
        price = prices[sku]

        assert isinstance(price, dict)
        assert "buy" in price
        assert "sell" in price
        assert "keys" in price["buy"]
        assert "metal" in price["buy"]
        assert "keys" in price["sell"]
        assert "metal" in price["sell"]
        break
