from tf2_utils import BackpackTFSocket


def my_function(data: dict):
    print("got data!", data)


socket = BackpackTFSocket(my_function)

socket.listen()
