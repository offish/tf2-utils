from src.tf2_utils import SchemaItemsUtils

schema = SchemaItemsUtils()  # uses local files by default


def test_map_defindex_names() -> None:
    response = schema.map_defindex_name()
    assert {} != response


def test_name_to_sku_pure() -> None:
    assert schema.name_to_sku("Refined Metal") == "5002;6"
    assert schema.name_to_sku("Reclaimed Metal") == "5001;6"
    assert schema.name_to_sku("Scrap Metal") == "5000;6"


def test_name_non_existing_item() -> None:
    item_name = "Non-Craftable Strange Team Captain"

    assert schema.name_to_sku(item_name) == "378;11;uncraftable"
    assert schema.name_to_defindex(item_name) == -1


def test_name_to_sku_qualities() -> None:
    assert schema.name_to_sku("Genuine Team Captain") == "378;1"
    assert schema.name_to_sku("Vintage Team Captain") == "378;3"
    assert schema.name_to_sku("Team Captain") == "378;6"
    assert schema.name_to_sku("Strange Team Captain") == "378;11"
    assert schema.name_to_sku("Haunted Team Captain") == "378;13"
    assert schema.name_to_sku("Collector's Team Captain") == "378;14"


def test_defindex_to_name() -> None:
    assert schema.defindex_to_name(378) == "Team Captain"
    assert schema.defindex_to_name(725) == "Tour of Duty Ticket"
    assert schema.defindex_to_name(5021) == "Mann Co. Supply Crate Key"
    assert schema.defindex_to_name(-100) == "Random Craft Hat"
    assert schema.defindex_to_name(-50) == "Random Craft Weapon"
    assert schema.defindex_to_name(5000) == "Scrap Metal"
    assert schema.defindex_to_name(5001) == "Reclaimed Metal"
    assert schema.defindex_to_name(5002) == "Refined Metal"


def test_tod_sku() -> None:
    assert schema.sku_to_base_name("725;6;uncraftable") == "Tour of Duty Ticket"
    assert schema.sku_to_name("725;6;uncraftable") == "Uncraftable Tour of Duty Ticket"
    assert (
        schema.sku_to_name("725;6;uncraftable", as_uncraftable=False)
        == "Non-Craftable Tour of Duty Ticket"
    )


def test_team_captain() -> None:
    assert schema.sku_to_base_name("378;6"), "Team Captain"
    assert schema.sku_to_full_name("378;6"), "The Team Captain"
    assert schema.sku_to_name("378;6"), "Team Captain"
    assert schema.sku_to_name("378;6;uncraftable"), "Uncraftable Team Captain"


def test_image_url() -> None:
    assert schema.defindex_to_image_url(263)
    assert schema.defindex_to_image_url(263, True) != schema.defindex_to_image_url(263)
    assert schema.sku_to_image_url("-100;6")
    assert schema.defindex_to_image_url(263) == schema.sku_to_image_url("-100;6")
    assert schema.sku_to_image_url("5021;6")
    assert not schema.defindex_to_image_url(-1)
    assert not schema.sku_to_image_url("-1;6")


def test_name_to_sku() -> None:
    assert schema.name_to_sku("Mann Co. Supply Crate Key") == "5021;6"
    assert schema.name_to_sku("Uncraftable Tour of Duty Ticket") == "725;6;uncraftable"
    assert schema.name_to_sku("Tour of Duty Ticket") == "725;6"
    assert schema.name_to_sku("Max's Severed Head") == "162;6"
    assert schema.name_to_sku("Name Tag") == "5020;6"
    assert schema.name_to_sku("Taunt: The Schadenfreude") == "463;6"
    assert schema.name_to_sku("Paint: Australium Gold") == "5037;6"
    assert (
        schema.name_to_sku("Uncraftable Paint: An Extraordinary Abundance of Tinge")
        == "5039;6;uncraftable"
    )
    assert schema.name_to_sku("Earbuds") == "143;6"
    assert schema.name_to_sku("Uncraftable Ap-Sap") == "933;6;uncraftable"
    assert schema.name_to_sku("Professional Black Rose") == "727;6;kt-3"
    assert schema.name_to_sku("Uncraftable Festivizer") == "5839;6;uncraftable"
    assert schema.name_to_sku("Scorching Flames Killer Exclusive") == "538;5;u14"
    assert schema.name_to_sku("Holy Grail Taunt: The Victory Lap") == "1172;5;u3003"
    assert schema.name_to_sku("Strange Stormy Storm Bonk Boy") == "451;5;u29;strange"
    assert schema.name_to_sku("Strange Festive Sandvich") == "1002;11"
    assert (
        schema.name_to_sku("Professional Collector's Festivized Tomislav")
        == "424;14;kt-3;festive"
    )
    assert (
        schema.name_to_sku("Professional Strange Festive Rocket Launcher")
        == "658;11;kt-3"
    )
    assert (
        schema.name_to_sku("Professional Festivized Australium Sniper Rifle")
        == "201;11;australium;kt-3;festive"
    )
    assert schema.name_to_sku("Professional Genuine Original") == "513;1;kt-3"
    assert schema.name_to_sku("Genuine Texas Ten Gallon") == "94;1"
    assert schema.name_to_sku("Professional Vintage Lugermorph") == "160;3;kt-3"


def test_sku_to_name() -> None:
    assert schema.sku_to_name("5021;6") == "Mann Co. Supply Crate Key"
    assert schema.sku_to_name("725;6;uncraftable") == "Uncraftable Tour of Duty Ticket"
    assert schema.sku_to_name("725;6") == "Tour of Duty Ticket"
    assert schema.sku_to_name("162;6") == "Max's Severed Head"
    assert schema.sku_to_name("5020;6") == "Name Tag"
    assert schema.sku_to_name("463;6") == "Taunt: The Schadenfreude"
    assert schema.sku_to_name("5037;6") == "Australium Gold"
    assert (
        schema.sku_to_name("5039;6;uncraftable")
        == "Uncraftable An Extraordinary Abundance of Tinge"
    )
    assert schema.sku_to_name("143;6") == "Earbuds"
    assert schema.sku_to_name("933;6;uncraftable") == "Uncraftable Ap-Sap"
    assert schema.sku_to_name("727;6;kt-3") == "Professional Black Rose"
    assert schema.sku_to_name("5839;6;uncraftable") == "Uncraftable Festivizer"
    assert schema.sku_to_name("538;5;u14") == "Scorching Flames Killer Exclusive"
    assert schema.sku_to_name("1172;5;u3003") == "Holy Grail Taunt: The Victory Lap"
    assert schema.sku_to_name("451;5;u29;strange") == "Strange Stormy Storm Bonk Boy"
    assert schema.sku_to_name("1002;11") == "Strange Festive Sandvich"
    assert (
        schema.sku_to_name("424;14;kt-3;festive")
        == "Professional Collector's Festivized Tomislav"
    )
    assert (
        schema.sku_to_name("658;11;kt-3")
        == "Professional Strange Festive Rocket Launcher"
    )
    assert (
        schema.sku_to_name("201;11;australium;kt-3;festive")
        == "Professional Festivized Australium Sniper Rifle"
    )
    assert schema.sku_to_name("513;1;kt-3") == "Professional Genuine Original"
    assert schema.sku_to_name("94;1") == "Genuine Texas Ten Gallon"
    assert schema.sku_to_name("160;3;kt-3") == "Professional Vintage Lugermorph"
