from tf2_data import EFFECTS, KILLSTREAKS, QUALITIES, SchemaItems
from tf2_sku import to_sku

from .sku import (
    get_sku_effect,
    get_sku_killstreak,
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

    def name_to_defindex(self, name: str) -> int:
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

        return defindexes[0]

    def defindex_to_image_url(self, defindex: int, large: bool = False) -> str:
        # random craft weapon => shotgun
        if defindex == -50:
            defindex = 9

        # random craft hat image => ellis' cap
        if defindex == -100:
            defindex = 263

        for item in self.schema_items:
            if item["defindex"] != defindex:
                continue

            return item["image_url"] if not large else item["image_url_large"]

        return ""

    def sku_to_image_url(self, sku: str, large: bool = False) -> str:
        defindex = sku_to_defindex(sku)
        return self.defindex_to_image_url(defindex, large)

    def name_to_sku(self, name: str) -> str:
        """This is not accurate, be careful when using this."""
        parts = name.split(" ")

        defindex = -1
        craftable = True
        quality = 6

        for part in parts:
            if part in ["Uncraftable", "Non-Craftable"]:
                craftable = False

            if part in QUALITIES:
                quality = QUALITIES[part]

        defindex_name = name

        while True:
            # try whole name, then remove everything till the
            # first space for each iteration if defindex
            # for that name doesnt exist

            # example:
            # Uncraftable Strange Team Captain => -1
            # Strange Team Captain => -1
            # Team Captain => 378 != -1, so break

            defindex = self.name_to_defindex(defindex_name)

            if defindex != -1:
                break

            try:
                index = defindex_name.index(" ")
            except ValueError:
                break

            defindex_name = defindex_name[index + 1 :]

        sku_properties = {
            "defindex": defindex,
            "quality": quality,
            "craftable": craftable,
        }

        return to_sku(sku_properties)

    def sku_to_base_name(self, sku: str) -> str:
        defindex = sku_to_defindex(sku)
        return self.defindex_to_name(defindex)

    def sku_to_full_name(self, sku: str) -> str:
        defindex = sku_to_defindex(sku)
        return self.defindex_to_full_name(defindex)

    def sku_to_name(self, sku: str, use_uncraftable: bool = True) -> str:
        name = self.sku_to_base_name(sku)
        craftable = ""
        quality = sku_to_quality_name(sku)
        effect = get_sku_effect(sku)
        killstreak = get_sku_killstreak(sku)
        strange = strange_in_sku(sku)

        if quality not in ["Unusual", "Unique"]:
            quality += " "
        else:
            quality = ""

        if effect != -1:
            effect = EFFECTS[str(effect)] + " "
        else:
            effect = ""

        if killstreak != -1:
            killstreak = KILLSTREAKS[str(killstreak)] + " "
        else:
            killstreak = ""

        if strange:
            strange = "Strange "
        else:
            strange = ""

        if sku_is_uncraftable(sku):
            if use_uncraftable:
                craftable = "Uncraftable "
            else:
                craftable = "Non-Craftable "

        festive = ""
        festivized = ""
        wear = ""

        # TODO: add killstreaks and other properties (strange unusual etc.)
        # festive
        # festivzed
        # wear

        return "".join(
            [killstreak, strange, festive, festivized, craftable, quality, name, wear]
        )
