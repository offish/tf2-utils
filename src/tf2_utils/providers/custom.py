from .provider import Provider


class Custom(Provider):
    def __init__(self, api_key: str, url: str) -> None:
        super().__init__(api_key)
        self.url = url.rstrip("/")

    def get_url_and_params(
        self, steam_id: str, app_id: int, context_id: int
    ) -> tuple[str, dict]:
        return (
            f"{self.url}/inventory/{steam_id}/{app_id}/{context_id}",
            {"api_key": self.api_key} if self.api_key else {},
        )
