import requests
import json

data = {}
file = 'price.json'

def fixed_name(item_name):
    return item_name.replace(' ', '%20')

def get_item(appid, item_name):
    r = requests.get('https://steamcommunity.com/market/priceoverview/?currency=1&appid={}&market_hash_name={}'.format(appid, fixed_name(item_name))).json()
    if(r['success'] == True):
        data[item_name] = {
            'lowest_price': r['lowest_price'],
            'median_price': r['median_price']
        }
        return data
    else:
        return False

def get_lowest_price(appid, item_name):
    r = requests.get('https://steamcommunity.com/market/priceoverview/?currency=1&appid={}&market_hash_name={}'.format(appid, fixed_name(item_name))).json()
    if(r['success'] == True):
        return  r['lowest_price']
    else:
        return False

def get_median_price(appid, item_name):
    r = requests.get('https://steamcommunity.com/market/priceoverview/?currency=1&appid={}&market_hash_name={}'.format(appid, fixed_name(item_name))).json()
    if(r['success'] == True):
        return  r['median_price']
    else:
        return False

def get_volume(appid, item_name):
    r = requests.get('https://steamcommunity.com/market/priceoverview/?currency=1&appid={}&market_hash_name={}'.format(appid, fixed_name(item_name))).json()
    if(r['success'] == True):
        return r['volume'].replace(',', '')
    else:
        return False

item = 'Mann Co. Supply Crate Key'

print(get_item(440, item))
print(get_volume(440, item))
print(get_lowest_price(440, item))
print(get_median_price(440, item))

with open(file, 'w') as outfile:
    json.dump(data, outfile, indent=4)
