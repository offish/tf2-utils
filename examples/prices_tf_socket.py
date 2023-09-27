from tf2_utils import PricesTFSocket


def my_function(data: dict):
    print("got data!", data)


socket = PricesTFSocket(my_function)

socket.listen()
