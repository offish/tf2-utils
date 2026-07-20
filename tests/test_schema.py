from src.tf2_utils.instances import schema


def test_map_defindex_names() -> None:
    response = schema.map_defindex_name()
    assert {} != response


def test_get_sku_from_name_pure() -> None:
    assert schema.get_sku_from_name("Refined Metal") == "5002;6"
    assert schema.get_sku_from_name("Reclaimed Metal") == "5001;6"
    assert schema.get_sku_from_name("Scrap Metal") == "5000;6"


def test_name_non_existing_item() -> None:
    item_name = "Non-Craftable Strange Team Captain"

    assert schema.get_sku_from_name(item_name) == "378;11;uncraftable"
    assert schema.get_name_from_defindex(item_name) is None


def test_get_sku_from_name_qualities() -> None:
    assert schema.get_sku_from_name("Genuine Team Captain") == "378;1"
    assert schema.get_sku_from_name("Vintage Team Captain") == "378;3"
    assert schema.get_sku_from_name("Team Captain") == "378;6"
    assert schema.get_sku_from_name("Strange Team Captain") == "378;11"
    assert schema.get_sku_from_name("Haunted Team Captain") == "378;13"
    assert schema.get_sku_from_name("Collector's Team Captain") == "378;14"


def test_get_base_name_from_defindex() -> None:
    assert schema.get_base_name_from_defindex(378) == "Team Captain"
    assert schema.get_base_name_from_defindex(725) == "Tour of Duty Ticket"
    assert schema.get_base_name_from_defindex(5021) == "Mann Co. Supply Crate Key"
    assert schema.get_base_name_from_defindex(-100) == "Random Craft Hat"
    assert schema.get_base_name_from_defindex(-50) == "Random Craft Weapon"
    assert schema.get_base_name_from_defindex(5000) == "Scrap Metal"
    assert schema.get_base_name_from_defindex(5001) == "Reclaimed Metal"
    assert schema.get_base_name_from_defindex(5002) == "Refined Metal"


def test_tod_sku() -> None:
    assert schema.get_base_name_from_sku("725;6;uncraftable") == "Tour of Duty Ticket"
    assert (
        schema.get_name_from_sku("725;6;uncraftable")
        == "Uncraftable Tour of Duty Ticket"
    )
    assert (
        schema.get_name_from_sku("725;6;uncraftable", as_uncraftable=False)
        == "Non-Craftable Tour of Duty Ticket"
    )


def test_team_captain() -> None:
    assert schema.get_base_name_from_sku("378;6"), "Team Captain"
    assert schema.get_full_name_from_sku("378;6"), "The Team Captain"
    assert schema.get_name_from_sku("378;6"), "Team Captain"
    assert schema.get_name_from_sku("378;6;uncraftable"), "Uncraftable Team Captain"


def test_image_url() -> None:
    assert schema.get_image_url(263)
    assert schema.get_image_url(263, True) != schema.get_image_url(263)
    assert schema.get_image_url_from_sku("-100;6")
    assert schema.get_image_url(263) == schema.get_image_url_from_sku("-100;6")
    assert schema.get_image_url_from_sku("5021;6")
    assert not schema.get_image_url(-1)
    assert not schema.get_image_url_from_sku("-1;6")


def test_get_sku_from_name() -> None:
    assert schema.get_sku_from_name("Mann Co. Supply Crate Key") == "5021;6"
    assert (
        schema.get_sku_from_name("Uncraftable Tour of Duty Ticket")
        == "725;6;uncraftable"
    )
    assert schema.get_sku_from_name("Tour of Duty Ticket") == "725;6"
    assert schema.get_sku_from_name("Max's Severed Head") == "162;6"
    assert schema.get_sku_from_name("Name Tag") == "5020;6"
    assert schema.get_sku_from_name("Taunt: The Schadenfreude") == "463;6"
    assert schema.get_sku_from_name("Paint: Australium Gold") == "5037;6"
    assert (
        schema.get_sku_from_name(
            "Uncraftable Paint: An Extraordinary Abundance of Tinge"
        )
        == "5039;6;uncraftable"
    )
    assert schema.get_sku_from_name("Earbuds") == "143;6"
    assert schema.get_sku_from_name("Uncraftable Ap-Sap") == "933;6;uncraftable"
    assert schema.get_sku_from_name("Professional Black Rose") == "727;6;kt-3"
    assert schema.get_sku_from_name("Uncraftable Festivizer") == "5839;6;uncraftable"
    assert schema.get_sku_from_name("Scorching Flames Killer Exclusive") == "538;5;u14"
    assert (
        schema.get_sku_from_name("Holy Grail Taunt: The Victory Lap") == "1172;5;u3003"
    )
    assert (
        schema.get_sku_from_name("Strange Stormy Storm Bonk Boy") == "451;5;u29;strange"
    )
    assert schema.get_sku_from_name("Strange Festive Sandvich") == "1002;11"
    assert (
        schema.get_sku_from_name("Professional Collector's Festivized Tomislav")
        == "424;14;kt-3;festive"
    )
    assert (
        schema.get_sku_from_name("Professional Strange Festive Rocket Launcher")
        == "658;11;kt-3"
    )
    assert (
        schema.get_sku_from_name("Professional Festivized Australium Sniper Rifle")
        == "201;11;australium;kt-3;festive"
    )
    assert schema.get_sku_from_name("Professional Genuine Original") == "513;1;kt-3"
    assert schema.get_sku_from_name("Genuine Texas Ten Gallon") == "94;1"
    assert schema.get_sku_from_name("Professional Vintage Lugermorph") == "160;3;kt-3"
    assert schema.get_sku_from_name("Strange Part: Gib Kills") == "6013;6"


def test_get_name_from_sku() -> None:
    assert schema.get_name_from_sku("5021;6") == "Mann Co. Supply Crate Key"
    assert (
        schema.get_name_from_sku("725;6;uncraftable")
        == "Uncraftable Tour of Duty Ticket"
    )
    assert schema.get_name_from_sku("725;6") == "Tour of Duty Ticket"
    assert schema.get_name_from_sku("162;6") == "Max's Severed Head"
    assert schema.get_name_from_sku("5020;6") == "Name Tag"
    assert schema.get_name_from_sku("463;6") == "Taunt: The Schadenfreude"
    assert schema.get_name_from_sku("5037;6") == "Australium Gold"
    assert (
        schema.get_name_from_sku("5039;6;uncraftable")
        == "Uncraftable An Extraordinary Abundance of Tinge"
    )
    assert schema.get_name_from_sku("143;6") == "Earbuds"
    assert schema.get_name_from_sku("933;6;uncraftable") == "Uncraftable Ap-Sap"
    assert schema.get_name_from_sku("727;6;kt-3") == "Professional Black Rose"
    assert schema.get_name_from_sku("5839;6;uncraftable") == "Uncraftable Festivizer"
    assert schema.get_name_from_sku("538;5;u14") == "Scorching Flames Killer Exclusive"
    assert (
        schema.get_name_from_sku("1172;5;u3003") == "Holy Grail Taunt: The Victory Lap"
    )
    assert (
        schema.get_name_from_sku("451;5;u29;strange") == "Strange Stormy Storm Bonk Boy"
    )
    assert schema.get_name_from_sku("1002;11") == "Strange Festive Sandvich"
    assert (
        schema.get_name_from_sku("424;14;kt-3;festive")
        == "Professional Collector's Festivized Tomislav"
    )
    assert (
        schema.get_name_from_sku("658;11;kt-3")
        == "Professional Strange Festive Rocket Launcher"
    )
    assert (
        schema.get_name_from_sku("201;11;australium;kt-3;festive")
        == "Professional Festivized Australium Sniper Rifle"
    )
    assert schema.get_name_from_sku("513;1;kt-3") == "Professional Genuine Original"
    assert schema.get_name_from_sku("94;1") == "Genuine Texas Ten Gallon"
    assert schema.get_name_from_sku("160;3;kt-3") == "Professional Vintage Lugermorph"
    assert schema.get_name_from_sku("6013;6") == "Strange Part: Gib Kills"
