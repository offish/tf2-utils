from abc import ABC, abstractmethod


class Provider(ABC):
    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key
        self.headers = {}

    @abstractmethod
    def get_url_and_params(
        self, steam_id: str, app_id: int, context_id: int
    ) -> tuple[str, dict]:
        pass
