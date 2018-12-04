import urllib.request
import json
from datetime import datetime

cardsetUrlJSONTemplate = {"cdn_root":"","url":"","expire_time":0}
cardsetFetchUrlTemplate = "https://playartifact.com/cardset/<setid>/"
cardsetUrlTemplate = "somehostsomeurl"
setids = '00', '01'

for setid in setids:
  with open('cardsetUrl-' + setid + '.json', 'w+') as json_file:
    try:
      cardsetUrlJSON = json.load(json_file)
    except ValueError:
      cardsetUrlJSON = json.loads(json.dumps(cardsetUrlJSONTemplate))
      json.dump(cardsetUrlJSON, json_file, sort_keys=True, indent=2)

  if datetime.now() >= datetime.fromtimestamp(cardsetUrlJSON['expire_time']):
    with urllib.request.urlopen(cardsetFetchUrlTemplate.replace("<setid>", setid)) as res: 
      cardsetUrlJSON = json.loads(res.read())

    with open('cardsetUrl-'+ setid + '.json', 'w') as outfile:
      json.dump(cardsetUrlJSON, outfile, sort_keys=True, indent=2)

  cardsetUrl = cardsetUrlTemplate.replace("somehost", cardsetUrlJSON["cdn_root"]).replace("/someurl", cardsetUrlJSON["url"])

  print('importing card set ' + setid + ' from ' + cardsetUrl)

  with urllib.request.urlopen(cardsetUrl) as res:
    cardsetJSON = json.loads(res.read())

  with open('cardset-'+ setid+ '.json', 'w+') as outfile:
    json.dump(cardsetJSON, outfile, sort_keys=True, indent=2) 