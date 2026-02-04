from aiohttp import ClientSession

from src.tf2_utils.marketplace_tf import MarketplaceTF


async def test_fetch_data(aiohttp_session: ClientSession) -> None:
    sku = "5021;6"
    mplc = MarketplaceTF(aiohttp_session)
    data = await mplc.fetch_item(sku)

    assert "sku" in data
    assert "highest_buy_order" in data
    assert "lowest_price" in data
    assert "stock" in data
    assert data["sku"] == sku
    assert isinstance(data["highest_buy_order"], float)
    assert isinstance(data["lowest_price"], float)
    assert isinstance(data["stock"], int)
