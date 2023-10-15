import time

from tf2_data import SchemaItems
from tf2_sku import to_sku
import requests


class SchemaItems(SchemaItems):
    def __init__(
        self, schema_items: str | list[dict] = "", defindex_names: str | dict = ""
    ) -> None:
        super().__init__(schema_items, defindex_names)

    def defindex_to_image_url(self, defindex: int, large: bool = False) -> str:
        if isinstance(defindex, str):
            defindex = int(defindex)

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
        defindex = sku.split(";")[:-1][0]
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

            match part:
                case "Genuine":
                    quality = 1

                case "Vintage":
                    quality = 3

                case "Strange":
                    quality = 11

        defindex_name = name

        while True:
            defindex = self.defindex_names.get(defindex_name, -1)

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


class IEconItems:
    API_URL = "https://api.steampowered.com/IEconItems_440"
    SCHEMA_OVERVIEW = API_URL + "/GetSchemaOverview/v0001"
    PLAYER_ITEMS = API_URL + "/GetPlayerItems/v0001"
    SCHEMA_ITEMS = API_URL + "/GetSchemaItems/v1"
    STORE_DATA = API_URL + "/GetStoreMetaData/v1"
    SCHEMA_URL = API_URL + "/GetSchemaURL/v1"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def __get(self, url: str, params: dict = {}) -> dict:
        params["key"] = self.api_key

        res = requests.get(url, params=params)

        try:
            return res.json()
        except:
            return {}

    def get_player_items(self, steamid: str) -> dict:
        return self.__get(self.PLAYER_ITEMS, {"steamid": steamid})

    def get_schema_items(self, start: int = 0, language: str = "en") -> dict:
        return self.__get(
            self.SCHEMA_ITEMS, {"language": language.lower(), "start": start}
        )

    def get_all_schema_items(self, language: str = "en", sleep: float = 5.0) -> list:
        items = []
        start = 0

        while start is not None:
            response = self.get_schema_items(start, language=language)["result"]
            items += response.get("items", [])
            start = response.get("next")  # None if not found
            time.sleep(sleep)

        return items

    def get_schema_overview(self, language: str = "en") -> dict:
        return self.__get(self.SCHEMA_OVERVIEW, {"language": language.lower()})

    def get_schema_url(self) -> dict:
        return self.__get(self.SCHEMA_URL, {})

    def get_store_meta_data(self, language: str = "en") -> dict:
        return self.__get(self.STORE_DATA, {"language": language.lower()})
