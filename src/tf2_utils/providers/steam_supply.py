from .provider import Provider


class SteamSupply(Provider):
    def get_url_and_params(
        self, steam_id: str, app_id: int, context_id: int
    ) -> tuple[str, dict]:
        return (
            f"https://steam.supply/API/{self.api_key}/loadinventory",
            {"steamid": steam_id, "appid": app_id, "contextid": context_id},
        )
