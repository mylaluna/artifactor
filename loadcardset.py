import urllib.request
import json
import os
import sys
from datetime import datetime

try:
  import requests
except ImportError:
  sys.exit("""You need module requests! please run pip3 install requests.""")

cardsetUrlJSONTemplate = {"cdn_root":"","url":"","expire_time":0}
cardsetFetchUrlTemplate = "https://playartifact.com/cardset/<setid>/"
cardsetUrlTemplate = "somehostsomeurl"
setids = '00', '01'

for setid in setids:
  # pull cardsetUrlJSON from local file or Artifact API
  with open('cardsetUrl-' + setid + '.json', 'w+') as json_file:
    try:
      cardsetUrlJSON = json.load(json_file)
    except ValueError:
      cardsetUrlJSON = json.loads(json.dumps(cardsetUrlJSONTemplate))
      json.dump(cardsetUrlJSON, json_file, sort_keys=True, indent=2)
  
  # if cardsetUrlJSON has expired, request a new API and save it to file
  if datetime.now() >= datetime.fromtimestamp(cardsetUrlJSON['expire_time']):
    with urllib.request.urlopen(cardsetFetchUrlTemplate.replace("<setid>", setid)) as res: 
      cardsetUrlJSON = json.loads(res.read())

    with open('cardsetUrl-'+ setid + '.json', 'w') as outfile:
      json.dump(cardsetUrlJSON, outfile, sort_keys=True, indent=2)

  cardsetUrl = cardsetUrlTemplate.replace("somehost", cardsetUrlJSON["cdn_root"]).replace("/someurl", cardsetUrlJSON["url"])

  print('importing card set ' + setid + ' from ' + cardsetUrl)

  # pull cardsetJSON
  with urllib.request.urlopen(cardsetUrl) as res:
    cardsetJSON = json.loads(res.read())
  
  # save cardsetJSON to file
  with open('cardset-'+ setid+ '.json', 'w+') as outfile:
    json.dump(cardsetJSON, outfile, sort_keys=True, indent=2)

  # pull card images from cardsetJSON 
  # if not os.path.exists('cardset_image'):
  #   os.makedirs('cardset_image/' + setid + '/default/large_image')
  #   os.makedirs('cardset_image/' + setid + '/default/mini_image')
  #   os.makedirs('cardset_image/' + setid + '/schinese/large_image')
  #   os.makedirs('cardset_image/' + setid + '/schinese/mini_image')
  
  for card in cardsetJSON['card_set']['card_list']:
    # for language, name in card['card_name'].items():
    
    # ingame_image

    # large_image
    for language, image_url in card['large_image'].items():
      if language == 'default':
        language_dir = 'english'
        card_name = card['card_name']['english']
      else:
        language_dir = language
        card_name = card['card_name'][language]
      
      image_path = os.path.join('cardset_image', setid, language_dir, 'large_image', card_name, '.png')
      image_dir = os.path.dirname(image_path)
      if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        
      with open(image_path, 'wb') as imagefile:
        imagefile.write(requests.get(image_url).content)
    # mini_image


  

   