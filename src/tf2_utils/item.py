from tf2_data import (
    CRATE_SERIES,
    EFFECTS,
    KILLSTREAKERS,
    KILLSTREAKS,
    QUALITIES,
    SHEENS,
    WAR_PAINTS,
    WEARS,
)

from .constants import KEY, REC, REF, SCRAP
from .item_name import (
    get_killstreak_tier_from_name,
    has_australium_in_name,
    has_festivized_in_name,
    has_strange_in_name,
)


class Item:
    def __init__(self, item: dict) -> None:
        self.item = item
        self.name = item["market_hash_name"]
        self.descriptions = item.get("descriptions", [])
        self.tags = item.get("tags", [])

    def is_tf2(self) -> bool:
        return int(self.item["appid"]) == 440

    def is_tradable(self) -> bool:
        return self.item.get("tradable", 1) == 1

    def has_name(self, name: str) -> bool:
        return self.name == name

    def has_description(
        self, description: str, color: str | None = "756b5e", exact: bool = True
    ) -> bool:
        for i in self.descriptions:
            desc = i["value"]

            if color != i.get("color"):
                continue

            if (description == desc) or (description in desc and not exact):
                return True

        return False

    def get_description(
        self, description: str, color: str | None = "756b5e"
    ) -> str | None:
        for i in self.descriptions:
            desc = i["value"]

            if color != i.get("color"):
                continue

            if description not in desc:
                continue

            return desc

    def get_description_and_replace(
        self, description: str, color: str | None = "756b5e"
    ) -> str:
        desc = self.get_description(description, color) or ""
        return desc.replace(description, "")

    def has_tag(self, tag: str, exact: bool = True) -> bool:
        for i in self.tags:
            item_tag = i["localized_tag_name"]

            if (item_tag == tag) or (tag in item_tag.lower() and not exact):
                return True

        return False

    def has_quality(self, quality: str) -> bool:
        return self.get_quality() == quality

    def has_strange_in_name(self) -> bool:
        return has_strange_in_name(self.name)

    def get_killstreak(self) -> str | None:
        killstreak = self.get_killstreak_tier()
        return KILLSTREAKS.get(str(killstreak))

    def get_quality(self) -> str | None:
        for tag in self.tags:
            if tag["localized_category_name"] != "Quality":
                continue

            return tag["localized_tag_name"]

    def get_quality_id(self) -> int:
        quality = self.get_quality()
        return QUALITIES.get(quality, -1)

    def get_defindex(self) -> int:
        for action in self.item["actions"]:
            if action["name"] != "Item Wiki Page...":
                continue

            wiki_link = action["link"]
            start = wiki_link.index("id=")
            end = wiki_link.index("lang=")
            defindex = wiki_link[start + 3 : end - 1]

            return int(defindex)

        return -1  # could not find

    def get_effect(self) -> str:
        return self.get_description_and_replace("\u2605 Unusual Effect: ", "ffd700")

    def get_effect_id(self) -> int:
        # cases will return an effect
        if not self.is_unusual():
            return -1

        effect = self.get_effect()
        return EFFECTS.get(effect, -1)

    def get_paint(self) -> str:
        return self.get_description_and_replace("Paint Color: ")

    def get_killstreak_tier(self) -> int:
        return get_killstreak_tier_from_name(self.name)

    def get_wear(self) -> str | None:
        for tag in self.tags:
            if tag["category"] != "Exterior":
                continue

            return tag["localized_tag_name"]

    def get_wear_id(self) -> int:
        wear = self.get_wear()
        return WEARS.get(wear, -1)

    def get_killstreaker(self) -> str:
        return self.get_description_and_replace("Killstreaker: ", "7ea9d1")

    def get_killstreaker_id(self) -> int:
        killstreaker = self.get_killstreaker()
        return KILLSTREAKERS.get(killstreaker, -1)

    def get_sheen(self) -> str:
        return self.get_description_and_replace("Sheen: ", "7ea9d1")

    def get_sheen_id(self) -> int:
        sheen = self.get_sheen()
        return SHEENS.get(sheen, -1)

    def get_skin(self) -> str | None:
        for war_paint in WAR_PAINTS:
            if war_paint in self.name:
                return war_paint

    def get_skin_id(self) -> int:
        skin = self.get_skin()
        return WAR_PAINTS.get(skin, -1)

    def get_crate_series(self) -> int:
        return CRATE_SERIES.get(self.name, -1)

    def is_genuine(self) -> bool:
        return self.has_quality("Genuine")

    def is_vintage(self) -> bool:
        return self.has_quality("Vintage")

    def is_unusual(self) -> bool:
        return self.has_quality("Unusual")

    def is_unique(self) -> bool:
        return self.has_quality("Unique")

    def is_strange(self) -> bool:
        return self.has_quality("Strange")

    def is_haunted(self) -> bool:
        return self.has_quality("Haunted")

    def is_collectors(self) -> bool:
        return self.has_quality("Collector's")

    def is_decorated_weapon(self) -> bool:
        return self.has_tag("Decorated Weapon")

    def is_craftable(self) -> bool:
        return not self.has_description("( Not Usable in Crafting )", None)  # no color

    def is_uncraftable(self) -> bool:
        return not self.is_craftable()

    def is_non_craftable(self) -> bool:
        return self.is_uncraftable()

    def is_painted(self) -> bool:
        return self.has_description("Paint Color: ", exact=False)

    def has_spell(self) -> bool:
        return self.has_description("(spell only active during event)", "7ea9d1", False)

    def is_special(self) -> bool:
        return self.is_painted() or self.has_spell()
        # or self.has_strange_part()

    def is_festivized(self) -> bool:
        return has_festivized_in_name(self.name)

    def is_halloween(self) -> bool:
        return self.has_description("Holiday Restriction: Halloween / Full Moon")

    def is_craft_weapon(self) -> bool:
        return (
            self.is_unique() and self.is_craftable() and self.has_tag("weapon", False)
        )

    def is_cosmetic(self) -> bool:
        return self.has_tag("Cosmetic")

    def is_craft_hat(self) -> bool:
        return (
            self.is_unique()
            and self.is_craftable()
            and self.is_cosmetic()
            and not self.is_halloween()
        )

    def is_unusual_cosmetic(self) -> bool:
        return self.is_unusual() and self.is_cosmetic()

    def is_australium(self) -> bool:
        return has_australium_in_name(self.name) and self.is_strange()

    def is_pure(self) -> bool:
        return (
            self.is_craftable()
            and self.is_unique()
            and self.name in [KEY, REF, REC, SCRAP]
        )

    def is_key(self) -> bool:
        return self.has_name(KEY) and self.is_craftable() and self.is_unique()

    def is_mann_co_key(self) -> bool:
        return self.is_key()

    def is_killstreak(self) -> bool:
        return self.get_killstreak_tier() != -1

    def is_basic_killstreak(self) -> bool:
        return self.get_killstreak_tier() == 1

    def is_specialized_killstreak(self) -> bool:
        return self.get_killstreak_tier() == 2

    def is_professional_killstreak(self) -> bool:
        return self.get_killstreak_tier() == 3
