class SteamCommunity:
    def __init__(self, api_key: str = "") -> None:
        pass  # we dont care about api_key for steam

    def get_url_and_params(
        self, steam_id: str, app_id: int, context_id: int
    ) -> tuple[str, dict]:
        return (
            f"https://steamcommunity.com/inventory/{steam_id}/{app_id}/{context_id}",
            {"l": "english", "count": 5000},
        )
