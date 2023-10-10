from .utils import read_json_file, write_json_file

import os

import requests


def get_json_path(name: str) -> str:
    # TODO: do more dynamic than schema.py?
    return os.path.abspath(__file__).replace("schema.py", "") + f"/json/{name}.json"


def use_local_json(name: str) -> dict | list:
    return read_json_file(get_json_path(name))


ITEM_QUALITIES = use_local_json("qualities")
SCHEMA_PATH = get_json_path("schema")
EFFECTS = use_local_json("effects")


class Schema:
    def __init__(self, schema: dict | str = {}, api_key: str = "") -> None:
        if not schema:
            if api_key:
                schema = IEconItems(api_key).get_schema_overview(save_file=True)
            else:
                schema = SCHEMA_PATH

        if isinstance(schema, str):
            schema = read_json_file(schema)

        self.schema = schema

    def set_effects(self) -> dict:
        path = get_json_path("effects")
        effects = self.schema["result"]["attribute_controlled_attached_particles"]

        data = {}

        for effect in effects:
            effect_name = effect["name"]
            effect_id = effect["id"]

            # map both ways for ease of use
            data[effect_name] = effect_id
            data[effect_id] = effect_name

        write_json_file(path, data)
        return data

    def set_qualities(self) -> dict:
        path = get_json_path("qualities")
        qualtiy_ids = self.schema["result"]["qualities"]
        qualtiy_names = self.schema["result"]["qualityNames"]

        data = {}

        for q in qualtiy_ids:
            quality_name = qualtiy_names[q]
            quality_id = qualtiy_ids[q]

            # map both ways for ease of use
            data[quality_name] = quality_id
            data[quality_id] = quality_name

        write_json_file(path, data)
        return data


class IEconItems:
    API_URL = "https://api.steampowered.com/IEconItems_440/"
    SCHEMA_OVERVIEW = API_URL + "GetSchemaOverview/v0001"
    PLAYER_ITEMS = API_URL + "GetPlayerItems/v0001"
    SCHEMA_ITEMS = API_URL + "GetSchemaItems/v1"
    STORE_DATA = API_URL + "GetStoreMetaData/v1"
    SCHEMA_URL = API_URL + "GetSchemaURL/v1"

    def __init__(self, key: str) -> None:
        self.key = key

    def __get(self, url: str, params: dict = {}) -> dict:
        params["key"] = self.key

        res = requests.get(url, params=params)

        try:
            return res.json()
        except:
            return {}

    def get_player_items(self, steamid: str) -> dict:
        return self.__get(self.PLAYER_ITEMS, {"steamid": steamid})

    def get_schema_items(self, language: str = "en") -> dict:
        return self.__get(self.SCHEMA_ITEMS, {"language": language.lower()})

    def get_schema_overview(
        self, language: str = "en", save_file: bool = False
    ) -> dict:
        schema = self.__get(self.SCHEMA_OVERVIEW, {"language": language.lower()})

        if schema and save_file:
            write_json_file(SCHEMA_PATH, schema)

        return schema

    def get_schema_url(self) -> dict:
        return self.__get(self.SCHEMA_URL, {})

    def get_store_meta_data(self, language: str = "en") -> dict:
        return self.__get(self.STORE_DATA, {"language": language.lower()})
