from src.tf2_utils import Item, get_sku


def test_craft_hat(ellis_cap: dict) -> None:
    item = Item(ellis_cap)

    assert item.is_craft_hat()
    assert not item.is_special()
    assert not item.is_painted()
    assert get_sku(item) == "263;6"


def test_uncraftable_hat(uncraftable_hat: dict) -> None:
    item = Item(uncraftable_hat)

    assert item.is_uncraftable()
    assert not item.is_craftable()
    assert not item.is_craft_hat()


def test_painted(painted_hat: dict) -> None:
    item = Item(painted_hat)

    assert item.is_painted()
    assert item.is_special()
    assert item.get_paint() == "Australium Gold"
    assert item.is_craft_hat()


def test_spell(spelled_item: dict) -> None:
    item = Item(spelled_item)

    assert item.is_special()
    assert item.has_spell()
    assert item.is_strange()
    # assert item.get_spell() == "Exorcism"


def test_unusual(hong_kong_cone: dict) -> None:
    item = Item(hong_kong_cone)

    assert item.is_unusual()
    assert not item.is_strange()
    assert item.get_effect() == "Neutron Star"
    assert item.get_paint() == "An Extraordinary Abundance of Tinge"
    assert not item.is_craft_hat()
    assert item.has_strange_in_name()
