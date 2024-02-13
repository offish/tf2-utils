import requests
import time

from .utils import to_refined


class PricesTFError(Exception):
    """General error"""


class InternalServerError(PricesTFError):
    """Something went wrong"""


class RateLimited(PricesTFError):
    """Rate limited"""


class EmptyResponse(PricesTFError):
    """Response was empty"""


class PricesTF:
    URL = "https://api2.prices.tf"

    def __init__(self) -> None:
        self.access_token = ""
        self.header = {}

    @staticmethod
    def has_code(response, code: int) -> bool:
        return response.get("statusCode") == code

    @staticmethod
    def validate_response(response) -> None:
        if not response:
            raise EmptyResponse("response from server was empty")

        if PricesTF.has_code(response, 500):
            raise InternalServerError("there was an interal server error")

        if PricesTF.has_code(response, 429):
            raise RateLimited("currently ratelimited")

    def __get(self, endpoint: str, params: dict = {}) -> dict:
        response = requests.get(self.URL + endpoint, headers=self.header, params=params)

        res = response.json()

        self.validate_response(res)
        return res

    def __post(self, endpoint: str) -> tuple[dict, int]:
        response = requests.post(self.URL + endpoint, headers=self.header)

        res = response.json()

        self.validate_response(res)
        return (res, response.status_code)

    def __set_header(self, header: dict) -> None:
        self.header = header

    def get_headers(self) -> dict:
        return self.header

    def get_history(
        self, sku: str, page: int = 1, limit: int = 100, order: str = "ASC"
    ) -> dict:
        return self.__get(
            f"/history/{sku}", {"page": page, "limit": limit, "order": order}
        )

    def get_price(self, sku: str) -> dict:
        return self.__get(f"/prices/{sku}")

    def get_prices(self, page: int, limit: int = 100, order: str = "DESC") -> dict:
        return self.__get("/prices", {"page": page, "limit": limit, "order": order})

    def format_price(self, data: dict) -> dict:
        return {
            "buy": {
                "keys": data["buyKeys"],
                "metal": to_refined(data["buyHalfScrap"] / 2),
            },
            "sell": {
                "keys": data["sellKeys"],
                "metal": to_refined(data["sellHalfScrap"] / 2),
            },
        }

    def get_prices_till_page(
        self, page_limit: int, print_rate_limit: bool = False
    ) -> dict:
        prices = {}
        current_page = 1
        # set higher than current page first time
        max_page = page_limit if page_limit != -1 else 2

        while current_page < max_page:
            try:
                response = self.get_prices(current_page)
            except RateLimited:
                timeout = 60

                if print_rate_limit:
                    print(f"rate limited from prices.tf, waiting {timeout} seconds")

                time.sleep(timeout)
                continue

            if "items" not in response:
                raise PricesTFError("could not find any items in response")

            for item in response["items"]:
                prices[item["sku"]] = self.format_price(item)

            current_page = response["meta"]["currentPage"] + 1
            total_pages = response["meta"]["totalPages"]

            if page_limit == -1:
                max_page = total_pages

        return prices

    def get_all_prices(self, print_rate_limit: bool = False) -> dict:
        return self.get_prices_till_page(-1, print_rate_limit)

    def update_price(self, sku: str) -> tuple[dict, int]:
        return self.__post(f"/prices/{sku}/refresh")

    def request_access_token(self) -> None:
        res, _ = self.__post("/auth/access")

        self.validate_response(res)

        access_token = res["accessToken"]
        self.access_token = access_token

        self.__set_header(
            {
                "accept": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            }
        )
