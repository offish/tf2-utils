from .utils import read_json_file, write_json_file

import json
import os

import requests


def _get_json_path(name: str) -> str:
    return os.path.abspath(__file__).replace("schema.py", "") + f"/json/{name}.json"


def _use_local_json(name: str) -> dict | list:
    return read_json_file(_get_json_path(name))


SCHEMA_PATH = _get_json_path("schema")
ITEM_QUALITIES = _use_local_json("qualities")
EFFECTS = _use_local_json("effects")


class Schema:
    def __init__(self, schema: dict | str = {}, api_key: str = "") -> None:
        if not schema:
            if api_key:
                schema = IEconItems(api_key).get_schema_overview(save_locally=True)
            else:
                schema = SCHEMA_PATH

        if isinstance(schema, str):
            schema = json.loads(open(schema, "r").read())

        self.schema = schema

    def set_effects(self) -> list[dict]:
        path = _get_json_path("effects")
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

    def set_qualities(self) -> None:
        path = _get_json_path("qualities")
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
    PLAYER_ITEMS = "http://api.steampowered.com/IEconItems_440/GetPlayerItems/v0001"
    SCHEMA_ITEMS = "https://api.steampowered.com/IEconItems_440/GetSchemaItems/v1"
    SCHEMA_OVERVIEW = (
        "https://api.steampowered.com/IEconItems_440/GetSchemaOverview/v0001"
    )
    SCHEMA_URL = "http://api.steampowered.com/IEconItems_440/GetSchemaURL/v1"
    STORE_DATA = "http://api.steampowered.com/IEconItems_440/GetStoreMetaData/v1"

    def __init__(self, key: str) -> None:
        self.key = key

    def _get(self, url: str, params: dict = {}) -> dict:
        params["key"] = self.key

        res = requests.get(url, params=params)

        try:
            return res.json()
        except:
            return {}

    def get_player_items(self, steamid: str) -> dict:
        return self._get(self.PLAYER_ITEMS, {"steamid": steamid})

    def get_schema_items(self, language: str = "en") -> dict:
        return self._get(self.SCHEMA_ITEMS, {"language": language.lower()})

    def get_schema_overview(
        self, language: str = "en", save_file: bool = False
    ) -> dict:
        schema = self._get(self.SCHEMA_OVERVIEW, {"language": language.lower()})

        if schema and save_file:
            write_json_file(SCHEMA_PATH, schema)

        return schema

    def get_schema_url(self) -> dict:
        return self._get(self.SCHEMA_URL, {})

    def get_store_meta_data(self, language: str = "en") -> dict:
        return self._get(self.STORE_DATA, {"language": language.lower()})
