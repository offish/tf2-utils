from tf2_utils import BackpackTFSocket


def my_function(data: list[dict]):
    print("got listings")

    for listing in data:
        print("listing", listing)

    # your logic here


socket = BackpackTFSocket(my_function, solo_entries=False)
# if solo_entries is True, you'll get a single dict instead of a list of dicts

socket.listen()
