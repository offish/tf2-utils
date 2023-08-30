import re


class Item:
    def __init__(self, item: dict) -> None:
        self.item = item
        self.name = item["market_hash_name"]
        self.descriptions = item.get("descriptions")

    def is_tf2(self) -> bool:
        return self.item["appid"] == 440

    def has_name(self, name: str) -> bool:
        return self.name == name

    def has_description(self, description: str) -> bool:
        if self.descriptions is None:
            return False

        for i in self.descriptions:
            if i["value"] == description:
                return True
        return False

    def has_tag(self, tag: str, exact: bool = True) -> bool:
        for i in self.item["tags"]:
            item_tag = i["localized_tag_name"]
            if (item_tag == tag and exact) or (tag in item_tag.lower() and not exact):
                return True
        return False

    def has_quality(self, quality: str) -> bool:
        return self.get_quality() == quality

    def get_quality(self) -> str:
        for tag in self.item["tags"]:
            if tag["localized_category_name"] != "Quality":
                continue
            return tag["localized_tag_name"]
        return ""  # could not find

    def get_defindex(self) -> int:
        for action in self.item["actions"]:
            if action["name"] == "Item Wiki Page...":
                link = action["link"]
                defindex = re.findall("\\d+", link)[0]
                return int(defindex)
        return -1  # could not find

    def get_effect(self) -> str:
        if not self.is_unusual():
            return ""

        string = "★ Unusual Effect: "

        if self.descriptions is None:
            return ""  # could not find

        for i in self.descriptions:
            if string in i["value"]:
                return i["value"].replace(string, "")
        return ""  # could not find

    def is_unique(self) -> bool:
        return self.has_quality("Unique")

    def is_unusual(self) -> bool:
        return self.has_quality("Unusual")

    def is_craftable(self) -> bool:
        return not self.has_description("( Not Usable in Crafting )")

    def is_halloween(self) -> bool:
        return self.has_description("Holiday Restriction: Halloween / Full Moon")

    def is_craft_weapon(self) -> bool:
        return (
            self.is_unique() and self.is_craftable() and self.has_tag("weapon", False)
        )

    def is_craft_hat(self) -> bool:
        return self.is_unique() and self.is_craftable() and self.has_tag("Cosmetic")

    def is_unusual_cosmetic(self) -> bool:
        return self.is_unusual() and self.has_tag("Cosmetic")

    def is_australium(self) -> bool:
        return "Australium" in self.name

    def is_strange(self) -> bool:
        return "Strange" in self.name

    def is_key(self) -> bool:
        return (
            self.is_craftable()
            and self.is_unique()
            and self.has_name("Mann Co. Supply Crate Key")
        )
