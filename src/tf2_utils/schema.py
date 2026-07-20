from tf2_data import SchemaItems
from tf2_sku import (
    get_defindex,
    has_australium_in_sku,
    has_festive_in_sku,
    has_strange_in_sku,
    is_uncraftable,
    to_sku,
)

from .item_name import (
    format_item_name,
    get_effect_in_name,
    get_killstreak_tier_from_name,
    get_quality_from_name,
    has_australium_in_name,
    has_festivized_in_name,
    has_strange_in_name,
    is_craftable,
)
from .sku import (
    get_effect_name_from_sku,
    get_killstreak_name_from_sku,
    sku_to_quality_name,
)

DEFINDEX_MAPPING = {
    "Random Craft Weapon": -50,
    "Random Craft Hat": -100,
    "Name Tag": 5020,
    "Mann Co. Supply Crate Key": 5021,
}


class SchemaItemsUtils(SchemaItems):
    def __init__(
        self, schema_items: str | list[dict] = "", defindex_names: str | dict = ""
    ) -> None:
        super().__init__(schema_items, defindex_names)

    @staticmethod
    def _get_name_from_defindex_mapping(defindex: int) -> str | None:
        for name, value in DEFINDEX_MAPPING.items():
            if value == defindex:
                return name

    def _get_name_from_defindex(self, defindex: int, data: dict) -> str | None:
        name = self._get_name_from_defindex_mapping(defindex)

        if not name:
            name = data.get(str(defindex))

        return name

    def get_base_name_from_defindex(self, defindex: int) -> str | None:
        return self._get_name_from_defindex(defindex, self.defindex_names)

    def get_full_name_from_defindex(self, defindex: int) -> str | None:
        return self._get_name_from_defindex(defindex, self.defindex_full_names)

    def get_name_from_defindex(self, defindex: int) -> str | None:
        return self.get_full_name_from_defindex(defindex)

    def get_defindex_from_base_name(self, name: str, index: int = 0) -> int | None:
        for key, defindex in DEFINDEX_MAPPING.items():
            if name == key:
                return defindex

        defindexes = self.defindex_names.get(name, [])

        if not defindexes:
            return

        if len(defindexes) == 1:
            return defindexes[0]

        return defindexes[index]

    def get_defindex_from_name(self, name: str, entry_index: int = 0) -> int | None:
        while True:
            defindex = self.get_defindex_from_base_name(name, entry_index)

            if defindex:
                return defindex

            index = name.find(" ")

            if index != -1:
                name = name[index + 1 :]

    def get_image_url(self, defindex: int, large_image: bool = False) -> str | None:
        # random craft weapon -> shotgun image
        if defindex == -50:
            defindex = 9

        # random craft hat -> ellis' cap image
        if defindex == -100:
            defindex = 263

        for item in self.schema_items:
            if item["defindex"] != defindex:
                continue

            image_url = item["image_url"]

            if large_image:
                image_url = item["image_url_large"]

            return image_url

    def get_image_url_from_sku(self, sku: str, large_image: bool = False) -> str:
        defindex = get_defindex(sku)
        return self.get_image_url(defindex, large_image)

    def get_sku_from_name(self, name: str) -> str:
        """This method is not accurate might return a wrong SKU."""
        quality = get_quality_from_name(name)
        defindex = self.get_defindex_from_name(name)
        effect = get_effect_in_name(name)
        is_australium = False

        if effect != -1:
            quality = 5

        # must be strange to be australium
        if has_australium_in_name(name):
            quality = 11
            is_australium = True

        # australium weapons are the second entry in the defindex list, get defindex again
        if is_australium:
            defindex = self.get_defindex_from_name(name, 1)

        sku_properties = {
            "defindex": defindex,
            "quality": quality,
            "effect": effect,
            "strange": has_strange_in_name(name) and quality != 11,
            "festivized": has_festivized_in_name(name),
            "craftable": is_craftable(name),
            "killstreak_tier": get_killstreak_tier_from_name(name),
            "australium": is_australium,
        }

        return to_sku(sku_properties)

    def get_base_name_from_sku(self, sku: str) -> str:
        defindex = get_defindex(sku)
        return self.get_base_name_from_defindex(defindex)

    def get_full_name_from_sku(self, sku: str) -> str:
        defindex = get_defindex(sku)
        return self.get_full_name_from_defindex(defindex)

    def get_name_from_sku(self, sku: str, as_uncraftable: bool = True) -> str:
        """This method is not accurate might return an inaccurate item name."""
        name = self.get_base_name_from_sku(sku)
        quality = sku_to_quality_name(sku)
        craftable = None
        festivized = None
        effect = get_effect_name_from_sku(sku)
        killstreak = get_killstreak_name_from_sku(sku)
        is_australium = has_australium_in_sku(sku)
        strange = None

        if has_festive_in_sku(sku):
            festivized = "Festivized"

        if has_strange_in_sku(sku):
            strange = "Strange"

        # these do not appear in names on marketplace.tf
        # however, genuine, strange, vintage etc. does
        if quality in ["Unusual", "Unique"]:
            quality = None

        if is_australium:
            name = "Australium " + name
            quality = None

        if is_uncraftable(sku):
            craftable = "Uncraftable" if as_uncraftable else "Non-Craftable"

        return format_item_name(
            name,
            quality=quality,
            craftable=craftable,
            effect=effect,
            killstreak=killstreak,
            strange=strange,
            festivized=festivized,
        )
