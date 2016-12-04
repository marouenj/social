import requests

def people_info(api_key, user_id):
  url = 'https://api.flickr.com/services'
  params = {'api_key':api_key,'method':'flickr.people.getInfo','user_id':user_id,'format':'json'}
  resp = requests.get(url, params=params)
  return resp
