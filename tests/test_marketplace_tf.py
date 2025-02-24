from src.tf2_utils import MarketplaceTF

mplc = None


def test_initiate_marketplace_tf(marketplace_tf_api_key: str) -> None:
    global mplc
    mplc = MarketplaceTF(marketplace_tf_api_key)


def test_key_data() -> None:
    price = mplc.fetch_item("5021;6")

    assert mplc.get_sku() == "5021;6"
    assert mplc.get_stock() > 1
    assert mplc.get_price() > 1.4
    assert mplc.get_highest_buy_order() < 2.5
    assert mplc.get_item_data() == price
    assert mplc.get_lowest_price() == mplc.get_price()


# def test_no_api_key(self):
#     self.mplc.api_key = ""
#     endpoints = self.mplc.get_endpoints()

#     self.assertTrue("endpoints" in endpoints)
#     self.assertRaises(NoAPIKey, self.mplc.get_bots)
#     self.assertRaises(NoAPIKey, self.mplc.get_is_banned("76561198253325712"))
#     self.mplc.api_key = MARKETPLACE_TF_API_KEY

# def test_get_bots(self):
#     self.assertTrue(self.mplc.get_bots()["success"])

# def test_get_bans(self):
#     self.assertEqual("confern", self.mplc.get_name("76561198253325712"))
#     self.assertTrue(self.mplc.get_is_seller("76561198253325712"))
#     self.assertFalse(self.mplc.get_is_banned("76561198253325712"))
#     self.assertEqual(self.mplc.get_seller_id("76561198253325712"), 195002)

#     self.assertTrue(self.mplc.get_is_banned("76561198115857578"))
#     self.assertFalse(self.mplc.get_is_seller("76561198115857578"))

# def test_get_dashboard_items(self):
#     dashboard = self.mplc.get_dashboard_items()

#     self.assertTrue("items" in dashboard)
#     self.assertTrue(dashboard["success"])

# def test_get_sales(self):
#     sales = self.mplc.get_sales()

#     self.assertTrue("sales" in sales)
#     self.assertTrue(sales["success"])

#     sales = self.mplc.get_sales(number=1)
#     self.assertTrue(len(sales["sales"]) == 1)

#     sales = self.mplc.get_sales(start_before=0)
#     self.assertEqual(sales, {})
