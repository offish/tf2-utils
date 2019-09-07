from tf2utils.methods import request


def get_price(name: str, cur: int = 1, appid: int = 440) -> dict:
    overview = 'https://steamcommunity.com/market/priceoverview/'
    params = {'currency': cur, 'appid': appid, 'market_hash_name': name}
    return request(overview, params)
