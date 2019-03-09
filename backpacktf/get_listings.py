import requests
import json

token = 'apikey'

r = requests.get('https://backpack.tf/api/classifieds/listings/v1?token={}'.format(token)).json()

data = {}
file = 'listings.json'

for i in r['listings']:
    if (i['intent'] == 0):
        data[i['item']['name']] = {
            "buy": i['currencies']['metal']
        }
    else:
        data[i['item']['name']] = {
            "sell": i['currencies']['metal']
        }

with open(file, 'w') as outfile:
    json.dump(data, outfile, indent=4)
