import json
import math
from pathlib import Path


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


def is_half_scrap_price(metal: float) -> bool:
    return math.ceil(metal * 18) % 2 == 1


def swap_intent(intent: str) -> str:
    intent = intent.lower()
    assert intent in ["buy", "sell"]
    return "buy" if intent == "sell" else "sell"
