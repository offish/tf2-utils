from requests.structures import CaseInsensitiveDict

from .provider import Provider


class SteamCommunity(Provider):
    def __init__(self, api_key: str = "") -> None:
        super().__init__(api_key)
        self.headers = CaseInsensitiveDict(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
                "Accept": (
                    "text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/avif,image/webp,image/apng,*/*;q=0.8,"
                    "application/signed-exchange;v=b3;q=0.7"
                ),
                "Accept-Language": "en-US,en;q=0.9,ja;q=0.8,ms;q=0.7",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": "",
                "Host": "steamcommunity.com",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Referer": "https://steamcommunity.com/",
            }
        )

    def get_url_and_params(
        self, steam_id: str, app_id: int, context_id: int
    ) -> tuple[str, dict]:
        self.headers["Referer"] = (
            f"https://steamcommunity.com/profiles/{steam_id}/inventory"
        )
        return (
            f"https://steamcommunity.com/inventory/{steam_id}/{app_id}/{context_id}",
            {"l": "english", "count": 2500},
        )
