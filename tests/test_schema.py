from src.tf2_utils import SchemaItemsUtils

schema_items = SchemaItemsUtils()  # uses local files by default


def test_map_defindex_names() -> None:
    response = schema_items.map_defindex_name()
    assert {} != response


def test_name_to_sku_tod() -> None:
    sku = schema_items.name_to_sku("Uncraftable Tour of Duty Ticket")
    assert "725;6;uncraftable" == sku


def test_name_to_sku_key() -> None:
    sku = schema_items.name_to_sku("Mann Co. Supply Crate Key")
    assert "5021;6" == sku


def test_name_to_sku_name_tag() -> None:
    sku = schema_items.name_to_sku("Name Tag")
    assert "5020;6" == sku


def test_name_to_sku_pure() -> None:
    ref = schema_items.name_to_sku("Refined Metal")
    rec = schema_items.name_to_sku("Reclaimed Metal")
    scrap = schema_items.name_to_sku("Scrap Metal")

    assert "5002;6" == ref
    assert "5001;6" == rec
    assert "5000;6" == scrap


def test_name_to_sku_non_existing() -> None:
    # this item does not exist
    item_name = "Non-Craftable Strange Team Captain"
    sku = schema_items.name_to_sku(item_name)
    defindex = schema_items.name_to_defindex(item_name)

    assert "378;11;uncraftable" == sku
    assert -1 == defindex


def test_name_to_sku_qualities() -> None:
    unique = schema_items.name_to_sku("Team Captain")
    genuine = schema_items.name_to_sku("Genuine Team Captain")
    haunted = schema_items.name_to_sku("Haunted Team Captain")
    strange = schema_items.name_to_sku("Strange Team Captain")
    vintage = schema_items.name_to_sku("Vintage Team Captain")
    collectors = schema_items.name_to_sku("Collector's Team Captain")

    assert "378;1" == genuine
    assert "378;3" == vintage
    assert "378;6" == unique
    assert "378;11" == strange
    assert "378;13" == haunted
    assert "378;14" == collectors


def test_defindex_to_name() -> None:
    assert "Tour of Duty Ticket" == schema_items.defindex_to_name(725)
    assert "Mann Co. Supply Crate Key" == schema_items.defindex_to_name(5021)
    assert "Random Craft Hat" == schema_items.defindex_to_name(-100)
    assert "Random Craft Weapon" == schema_items.defindex_to_name(-50)
    assert "Scrap Metal" == schema_items.defindex_to_name(5000)
    assert "Reclaimed Metal" == schema_items.defindex_to_name(5001)
    assert "Refined Metal" == schema_items.defindex_to_name(5002)


def test_sku_to_base_name_tod() -> None:
    name = schema_items.sku_to_base_name("725;6;uncraftable")
    assert "Tour of Duty Ticket" == name


def test_sku_to_name_tod() -> None:
    name = schema_items.sku_to_name("725;6;uncraftable")
    assert "Uncraftable Tour of Duty Ticket" == name


def test_sku_to_non_craftable_name() -> None:
    name = schema_items.sku_to_name("725;6;uncraftable", use_uncraftable=False)
    assert "Non-Craftable Tour of Duty Ticket" == name


def test_sku_to_name_key() -> None:
    name = schema_items.sku_to_name("5021;6")
    assert "Mann Co. Supply Crate Key" == name


def test_team_captain() -> None:
    # craftable
    assert schema_items.sku_to_base_name("378;6"), "Team Captain"
    assert schema_items.sku_to_full_name("378;6"), "The Team Captain"
    assert schema_items.sku_to_name("378;6"), "Team Captain"
    # uncraftable
    assert schema_items.sku_to_name("378;6;uncraftable"), "Uncraftable Team Captain"
    # strange
    assert schema_items.sku_to_base_name("378;11"), "Team Captain"
    assert schema_items.sku_to_name("378;11"), "Strange Team Captain"


def test_image_equal() -> None:
    ellis_cap = schema_items.defindex_to_image_url(263)
    random_craft_hat = schema_items.sku_to_image_url("-100;6")
    assert ellis_cap, random_craft_hat
