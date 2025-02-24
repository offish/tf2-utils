from src.tf2_utils import BackpackTF, Currencies

bptf = None


def test_initiate_backpack_tf(backpack_tf_token: str) -> None:
    global bptf
    bptf = BackpackTF(backpack_tf_token, "76561198253325712")


def test_currencies() -> None:
    assert Currencies(1, 1.5).__dict__ == {"keys": 1, "metal": 1.5}
    assert Currencies().__dict__ == {"keys": 0, "metal": 0.0}
    assert Currencies(**{"metal": 10.55}).__dict__ == {"keys": 0, "metal": 10.55}


def test_construct_listing_item() -> None:
    assert bptf._construct_listing_item("263;6") == {
        "baseName": "Ellis' Cap",
        "craftable": True,
        "quality": {"id": 6},
        "tradable": True,
    }


def test_construct_listing() -> None:
    assert bptf._construct_listing(
        "263;6",
        "sell",
        {"keys": 1, "metal": 1.55},
        "my description",
        13201231975,
    ) == {
        "buyout": True,
        "offers": True,
        "promoted": False,
        "item": {
            "baseName": "Ellis' Cap",
            "craftable": True,
            "quality": {"id": 6},
            "tradable": True,
        },
        "currencies": {"keys": 1, "metal": 1.55},
        "details": "my description",
        "id": 13201231975,
    }

    assert bptf._construct_listing(
        "263;6", "buy", {"keys": 1, "metal": 1.55}, "my description"
    ) == {
        "buyout": True,
        "offers": True,
        "promoted": False,
        "item": {
            "baseName": "Ellis' Cap",
            "craftable": True,
            "quality": {"id": 6},
            "tradable": True,
        },
        "currencies": {"keys": 1, "metal": 1.55},
        "details": "my description",
    }


def test_hash_name() -> None:
    assert bptf._get_sku_item_hash("5021;6") == "d9f847ff5dfcf78576a9fca04cbf6c07"
    assert bptf._get_sku_item_hash("30397;6") == "8010db121d19610e9bcbac47432bd78c"
    assert (
        bptf._get_item_hash("The Bruiser's Bandanna")
        == "8010db121d19610e9bcbac47432bd78c"
    )
