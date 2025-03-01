from src.tf2_utils import MarketplaceTF

mplc = None


def test_init() -> None:
    global mplc
    mplc = MarketplaceTF()


def test_key_data() -> None:
    price = mplc.fetch_item("5021;6")

    assert mplc.get_sku() == "5021;6"
    assert mplc.get_stock() > 1
    assert mplc.get_price() > 1.4
    assert mplc.get_highest_buy_order() < 2.5
    assert mplc.get_item_data() == price
    assert mplc.get_lowest_price() == mplc.get_price()


# def test_no_api_key(marketplace_tf_api_key: str) -> None:
#     global mplc
#     mplc = MarketplaceTF()
#     endpoints = mplc.get_endpoints()

#     assert "endpoints" in endpoints

#     with pytest.raises(NoAPIKey):
#         mplc.get_bots()

#     with pytest.raises(NoAPIKey):
#         mplc.get_is_banned("76561198253325712")

#     mplc._api_key = marketplace_tf_api_key


# def test_get_bots() -> None:
#     assert mplc.get_bots()["success"]


# def test_get_bans() -> None:
#     assert "confern" == mplc.get_name("76561198253325712")
#     assert mplc.get_is_seller("76561198253325712")
#     assert not mplc.get_is_banned("76561198253325712")
#     assert mplc.get_seller_id("76561198253325712") == 195002

#     assert mplc.get_is_banned("76561198115857578")
#     assert not mplc.get_is_seller("76561198115857578")


# def test_get_dashboard_items() -> None:
#     dashboard = mplc.get_dashboard_items()

#     assert "items" in dashboard
#     assert dashboard["success"]


# def test_get_sales() -> None:
#     sales = mplc.get_sales()

#     assert "sales" in sales
#     assert sales["success"]

#     sales = mplc.get_sales(number=1)
#     assert len(sales["sales"]) == 1

#     sales = mplc.get_sales(start_before=0)
#     assert sales == {}
