from tf2utils.methods import request

def get_bots() -> dict:
    bots = 'https://api.tf2automatic.com/v1/bots'
    return request(bots)

def get_currencies() -> dict:
    key = 'https://api.tf2automatic.com/v1/currencies'
    return request(key)
