class SteamApis:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_url_and_params(
        self, steam_id: str, app_id: int, context_id: int
    ) -> tuple[str, dict]:
        return (
            f"https://api.steamapis.com/steam/inventory/{steam_id}/{app_id}/{context_id}",
            {"api_key": self.api_key},
        )
