import math
import json


def read_json_file(path: str) -> dict | list:
    data = {}

    with open(path, "r") as f:
        data = json.loads(f.read())

    return data


def write_json_file(path: str, data: dict | list) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def to_scrap(refined: float) -> int:
    return math.ceil(refined * 9)


def to_refined(scrap: int) -> float:
    return math.floor(scrap / 9 * 100) / 100


def refinedify(value: float) -> float:
    return math.floor((round(value * 9, 0) * 100) / 9) / 100


def account_id_to_steam_id(account_id: int | str) -> str:
    return str(76561197960265728 + int(account_id))
