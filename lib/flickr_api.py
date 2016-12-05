import re, requests

pattern = '^jsonFlickrApi\((.*)\)$'

def people_findByUsername(api_key, user_name):
  url = 'https://api.flickr.com/services/rest'
  params = {'api_key':api_key,'method':'flickr.people.findByUsername','user_id':user_name,'format':'json'}
  resp = requests.get(url, params=params)
  match = re.search(pattern, resp.text)
  return match.group(1)

def people_getPhotos(api_key, user_id, since):
  url = 'https://api.flickr.com/services/rest'
  params = {'api_key':api_key,'method':'flickr.people.getPhotos','user_id':user_id,'format':'json','min_upload_date':since}
  resp = requests.get(url, params=params)
  match = re.search(pattern, resp.text)
  return match.group(1)

def people_getPublicPhotos(api_key, user_id):
  url = 'https://api.flickr.com/services/rest'
  params = {'api_key':api_key,'method':'flickr.people.getPublicPhotos','user_id':user_id,'format':'json'}
  resp = requests.get(url, params=params)
  match = re.search(pattern, resp.text)
  return match.group(1)

def people_info(api_key, user_id):
  url = 'https://api.flickr.com/services/rest'
  params = {'api_key':api_key,'method':'flickr.people.getInfo','user_id':user_id,'format':'json'}
  resp = requests.get(url, params=params)
  return resp
