import json
import math
import re
import struct
from pathlib import Path
from typing import Any

__all__ = [
    "to_scrap",
    "to_refined",
    "refinedify",
    "get_account_id_from_trade_url",
    "get_steam_id_from_trade_url",
    "get_token_from_trade_url",
    "swap_intent",
    "normalize_item_name",
    "account_id_to_steam_id",
    "steam_id_to_account_id",
]


def to_scrap(refined: float) -> int:
    return math.ceil(refined * 9)


def to_refined(scrap: int) -> float:
    return math.floor(scrap / 9 * 100) / 100


def get_scrap_price(keys: int, metal: float, key_scrap_price: int) -> int:
    return keys * key_scrap_price + to_scrap(metal)


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


def swap_intent(intent: str) -> str:
    return "buy" if intent.lower() == "sell" else "sell"


def normalize_item_name(name: str, as_lower: bool = True) -> str:
    if as_lower:
        name = name.lower()

    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name


# implementation from steampy
# https://github.com/bukson/steampy/blob/master/steampy/utils.py#L48
def account_id_to_steam_id(account_id: str | int) -> str:
    first_bytes = int(account_id).to_bytes(4, byteorder="big")
    last_bytes = 0x1100001.to_bytes(4, byteorder="big")
    return str(struct.unpack(">Q", last_bytes + first_bytes)[0])


# implementation from steampy
# https://github.com/bukson/steampy/blob/master/steampy/utils.py#L54
def steam_id_to_account_id(steam_id: str | int) -> str:
    return str(struct.unpack(">L", int(steam_id).to_bytes(8, byteorder="big")[4:])[0])


def read_json_file(path: Path | str) -> Any:
    data = {}

    with open(path, "r") as f:
        data = json.loads(f.read())

    return data


def write_json_file(path: Path | str, data: dict | list) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
