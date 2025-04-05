import json
import math
import struct
from pathlib import Path

__all__ = [
    "to_scrap",
    "to_refined",
    "refinedify",
    "get_account_id_from_trade_url",
    "get_steam_id_from_trade_url",
    "get_token_from_trade_url",
    "account_id_to_steam_id",
    "steam_id_to_account_id",
]


def read_json_file(path: Path | str) -> dict | list:
    data = {}

    with open(path, "r") as f:
        data = json.loads(f.read())

    return data


def write_json_file(path: Path | str, data: dict | list) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def to_scrap(refined: float) -> int:
    return math.ceil(refined * 9)


def to_refined(scrap: int) -> float:
    return math.floor(scrap / 9 * 100) / 100


def refinedify(value: float) -> float:
    return math.floor((round(value * 9, 0) * 100) / 9) / 100


def get_account_id_from_trade_url(trade_url: str) -> str:
    partner_index = trade_url.index("?partner=") + 9
    token_index = trade_url.index("&token=")
    return trade_url[partner_index:token_index]


def get_steam_id_from_trade_url(trade_url: str) -> str:
    return account_id_to_steam_id(get_account_id_from_trade_url(trade_url))


def get_token_from_trade_url(trade_url: str) -> str:
    token_index = trade_url.index("&token=") + 7
    return trade_url[token_index:]


# implementation from bukson's steampy
def account_id_to_steam_id(account_id: str | int) -> str:
    first_bytes = int(account_id).to_bytes(4, byteorder="big")
    last_bytes = 0x1100001.to_bytes(4, byteorder="big")
    return str(struct.unpack(">Q", last_bytes + first_bytes)[0])


# implementation from bukson's steampy
def steam_id_to_account_id(steam_id: str | int) -> str:
    return str(struct.unpack(">L", int(steam_id).to_bytes(8, byteorder="big")[4:])[0])
