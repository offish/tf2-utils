from tf2_data import SchemaItems
from tf2_sku import to_sku

from .item_name import (
    get_effect_in_name,
    get_quality_from_name,
    has_australium_in_name,
    has_basic_killstreak_in_name,
    has_festivized_in_name,
    has_professional_killstreak_in_name,
    has_specialized_killstreak_in_name,
    has_strange_in_name,
    is_craftable,
)
from .sku import (
    australium_in_sku,
    festive_in_sku,
    get_effect_name_from_sku,
    get_killstreak_name_from_sku,
    sku_is_uncraftable,
    sku_to_defindex,
    sku_to_quality_name,
    strange_in_sku,
)


class SchemaItemsUtils(SchemaItems):
    def __init__(
        self, schema_items: str | list[dict] = "", defindex_names: str | dict = ""
    ) -> None:
        super().__init__(schema_items, defindex_names)

    def defindex_to_name(self, defindex: int) -> str:
        if defindex == -50:
            return "Random Craft Weapon"

        if defindex == -100:
            return "Random Craft Hat"

        return self.defindex_names.get(str(defindex), "")

    def defindex_to_full_name(self, defindex: int) -> str:
        if defindex == 5021:
            return "Mann Co. Supply Crate Key"

        return self.defindex_full_names.get(str(defindex), "")

    def name_to_defindex(self, name: str, index: int = 0) -> int:
        if name == "Random Craft Weapon":
            return -50

        if name == "Random Craft Hat":
            return -100

        defindexes = self.defindex_names.get(name, [])

        if not defindexes:
            return -1

        has_multiple_defindexes = len(defindexes) != 1

        if not has_multiple_defindexes:
            return defindexes[0]

        last_index = len(defindexes) - 1

        if name == "Mann Co. Supply Crate Key":
            return defindexes[0]

        if name == "Name Tag":
            return defindexes[last_index]

        return defindexes[index]

    def defindex_to_image_url(self, defindex: int, large_image: bool = False) -> str:
        # random craft weapon => shotgun
        if defindex == -50:
            defindex = 9

        # random craft hat image => ellis' cap
        if defindex == -100:
            defindex = 263

        for item in self.schema_items:
            if item["defindex"] != defindex:
                continue

            return item["image_url_large"] if large_image else item["image_url"]

        return ""

    def sku_to_image_url(self, sku: str, large_image: bool = False) -> str:
        defindex = sku_to_defindex(sku)
        return self.defindex_to_image_url(defindex, large_image)

    def get_defindex_from_name(self, name: str, entry_index: int = 0) -> int:
        # try whole name, then remove everything till the
        # first space for each iteration if defindex
        # for that name doesnt exist

        # example:
        # Uncraftable Strange Team Captain => -1
        # Strange Team Captain => -1
        # Team Captain => 378 != -1, so break
        defindex_name = name
        defindex = -1

        while True:
            defindex = self.name_to_defindex(defindex_name, entry_index)

            if defindex != -1:
                break

            try:
                index = defindex_name.index(" ")
            except ValueError:
                break

            defindex_name = defindex_name[index + 1 :]

        return defindex

    def name_to_sku(self, name: str) -> str:
        quality = get_quality_from_name(name)
        defindex = self.get_defindex_from_name(name)
        effect = get_effect_in_name(name)
        is_australium = False
        killstreak_tier = -1

        if effect != -1:
            quality = 5

        if has_professional_killstreak_in_name(name):
            killstreak_tier = 3

        if has_specialized_killstreak_in_name(name):
            killstreak_tier = 2

        if has_basic_killstreak_in_name(name):
            killstreak_tier = 1

        # must be strange to be australium
        if "Australium Gold" not in name and has_australium_in_name(name):
            quality = 11
            is_australium = True

        # australium weapons are the second entry in the defindex list, need to
        # get the defindex again
        if is_australium:
            defindex = self.get_defindex_from_name(name, 1)

        sku_properties = {
            "defindex": defindex,
            "quality": quality,
            "effect": effect,
            "strange": has_strange_in_name(name) and quality != 11,
            "festivized": has_festivized_in_name(name),
            "craftable": is_craftable(name),
            "killstreak_tier": killstreak_tier,
            "australium": is_australium,
        }

        return to_sku(sku_properties)

    def sku_to_base_name(self, sku: str) -> str:
        defindex = sku_to_defindex(sku)
        return self.defindex_to_name(defindex)

    def sku_to_full_name(self, sku: str) -> str:
        defindex = sku_to_defindex(sku)
        return self.defindex_to_full_name(defindex)

    def format_name(
        self,
        item_name: str,
        quality: str = "",
        craftable: str = "",
        effect: str = "",
        killstreak: str = "",
        strange: str = "",
        festivized: str = "",
    ) -> str:
        return "".join(
            [killstreak, strange, effect, craftable, quality, festivized, item_name]
        )

    def sku_to_name(self, sku: str, as_uncraftable: bool = True) -> str:
        name = self.sku_to_base_name(sku)
        quality = sku_to_quality_name(sku)
        craftable = ""
        festivized = "Festivized " if festive_in_sku(sku) else ""
        effect = get_effect_name_from_sku(sku)
        killstreak = get_killstreak_name_from_sku(sku)
        is_australium = australium_in_sku(sku)
        strange = ""

        if strange_in_sku(sku):
            strange = "Strange "

        if quality not in ["Unusual", "Unique"]:
            quality += " "
        else:
            quality = ""

        if is_australium:
            quality = ""
            name = "Australium " + name

        if sku_is_uncraftable(sku):
            if as_uncraftable:
                craftable = "Uncraftable "
            else:
                craftable = "Non-Craftable "

        return self.format_name(
            name,
            quality=quality,
            craftable=craftable,
            effect=effect,
            killstreak=killstreak,
            strange=strange,
            festivized=festivized,
        )
