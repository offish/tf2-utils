import pytest


@pytest.fixture
def marketplace_tf_api_key() -> str:
    return "api_key"


@pytest.fixture
def backpack_tf_token() -> str:
    return "backpack_tf_token"
