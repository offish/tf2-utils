import requests
import json

data = []
file = 'bots.json'

r = requests.get('https://marketplace.tf/api/Bots/GetBots/v1').json()

if r['success'] == True:
    for i in r['steamids']:
        data.append(i)
    print('All Marketplace.tf bots were written to {}'.format(file))
else:
    print('Error. Wrong response from the API')

with open(file, 'w') as outfile:
    json.dump(data, outfile, indent=4)
