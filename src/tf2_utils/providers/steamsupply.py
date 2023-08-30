class SteamSupply:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_url_and_params(
        self, steam_id: str, app_id: int, context_id: int
    ) -> tuple[str, dict]:
        return (
            f"https://steam.supply/API/{self.api_key}/loadinventory",
            {"steamid": steam_id, "appid": app_id, "contextid": context_id},
        )
