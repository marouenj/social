import json, requests, sys, time

def user(token, user_id):
  url = 'https://api.foursquare.com/v2/users/' + user_id
  params = {'oauth_token': token, 'v':'20161116'}

  while True:
    r = requests.get(url, params=params)
    if r.status_code == 403:
      print('[WARN: ' + str(r.status_code) + '] Too many request')
      time.sleep(120)
    elif r.status_code != 200:
      print('[WARN: ' + str(r.status_code) + ':' + user_id + '] ' + r.text)
      return None
    else:
      return json.loads(r.text)
