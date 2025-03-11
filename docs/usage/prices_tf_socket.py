from tf2_utils import PricesTFWebsocket


def my_function(data: dict):
    print("got data!", data)

    data_type = data["type"]  # "PRICE_CHANGED","PRICE_UPDATED" etc.
    sku = data["data"]["sku"]  # 30035;6
    buy_half_scrap = data["data"]["buyHalfScrap"]  # 264
    # etc. your logic goes here


socket = PricesTFWebsocket(my_function)

socket.listen()

# flake8: noqa
