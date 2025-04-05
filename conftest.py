from os import getenv
from pathlib import Path

import pytest
from dotenv import load_dotenv

from src.tf2_utils.utils import read_json_file

assert load_dotenv()

MARKETPLACE_TF_API_KEY = getenv("MARKETPLACE_TF_API_KEY")
BACKPACK_TF_TOKEN = getenv("BACKPACK_TF_TOKEN")
EXPRESS_LOAD_API_KEY = getenv("EXPRESS_LOAD_API_KEY")


def get_item_data(file_name: str) -> dict:
    path = Path(__file__).parent / f"tests/json/{file_name}.json"
    return read_json_file(path)


# items
CRUSADERS_CROSSBOW = get_item_data("crusaders_crossbow")
UNCRAFTABLE_HAT = get_item_data("uncraftable_hat")
HONG_KONG_CONE = get_item_data("hong_kong_cone")
SPELLED_ITEM = get_item_data("spelled_item")
PAINTED_HAT = get_item_data("painted_hat")
ELLIS_CAP = get_item_data("ellis_cap")


@pytest.fixture
def steam_id() -> str:
    return "76561198253325712"


@pytest.fixture
def account_id() -> str:
    return "293059984"


@pytest.fixture
def marketplace_tf_api_key() -> str:
    return MARKETPLACE_TF_API_KEY


@pytest.fixture
def backpack_tf_token() -> str:
    return BACKPACK_TF_TOKEN


@pytest.fixture
def express_load_api_key() -> str:
    return EXPRESS_LOAD_API_KEY


# items
@pytest.fixture
def crusaders_crossbow() -> dict:
    return CRUSADERS_CROSSBOW


@pytest.fixture
def uncraftable_hat() -> dict:
    return UNCRAFTABLE_HAT


@pytest.fixture
def hong_kong_cone() -> dict:
    return HONG_KONG_CONE


@pytest.fixture
def spelled_item() -> dict:
    return SPELLED_ITEM


@pytest.fixture
def painted_hat() -> dict:
    return PAINTED_HAT


@pytest.fixture
def ellis_cap() -> dict:
    return ELLIS_CAP
