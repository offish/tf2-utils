import requests
import json

sell = 1
buy = 0

#key = 'Mann Co. Supply Crate Key'
#file = 'tetsstts.json'

r = requests.get('https://api.cash.tf/snapshots/5c8a855da9d9c2320f141172').json()

#data = []

def get_common_listing_price(result, intent):
    price = 0
    amt = 0
    for i in result['listings']:
        if i['intent'] == intent:
            price += float(i['currencies']['metal'])
            amt += 1
    return price / amt

def get_lowest_listing_price(result, intent):
    i = result['listings']
    if intent == 1:
        return i[0]['currencies']['metal']
    elif intent == 0:
        return i[len(i)-1]['currencies']['metal']

def get_steamids(result, intent):
    ids = []
    for i in result['listings']:
        if i['intent'] == intent:
            ids.append(i['steamid'])
    return ids

def get_value_from_id(result, steamid):
    data = {}
    for i in result['listings']:
        if i['steamid'] == steamid:
            data[steamid] = {
                get_intent(i['intent']): float(i['currencies']['metal'])
            }
            break
    return data

def get_intent(number):
    if number == 1:
        return 'sell'
    else:
        return 'buy'

def is_automatic(result, steamid):
    for i in result['listings']:
        if i['steamid'] == steamid:
            return i['automatic']

if r['success'] == True:
    print(get_common_listing_price(r, sell))
    print(get_lowest_listing_price(r, sell))
    print(get_steamids(r, sell))
    print(get_value_from_id(r, '76561198307684149'))
    print(is_automatic(r, '76561198307684149'))
else:
    print('There was an error when trying to access the API. Success: {}'.format(r['success']))

#with open(file, 'w') as outfile:
#    json.dump(data, outfile, indent=4)
