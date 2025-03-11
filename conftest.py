from os import getenv

import pytest
from dotenv import load_dotenv

assert load_dotenv()

MARKETPLACE_TF_API_KEY = getenv("MARKETPLACE_TF_API_KEY")
BACKPACK_TF_TOKEN = getenv("BACKPACK_TF_TOKEN")


@pytest.fixture
def marketplace_tf_api_key() -> str:
    return MARKETPLACE_TF_API_KEY


@pytest.fixture
def backpack_tf_token() -> str:
    return BACKPACK_TF_TOKEN
