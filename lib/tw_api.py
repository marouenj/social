import json, requests, sys

def users_show(token, user_id):
  url = 'https://api.twitter.com/1.1/users/show.json'
  params = {'user_id': user_id, 'include_entities': 'true'}
  headers= {'Authorization': 'Bearer ' + token}

  while True:
    r = requests.get(url, params=params, headers=headers)
    if r,status_code == 403:
      print('[WARN: ' + str(r.status_code) + '] ' + r.text)
      continue
    if r.status_code == 429:
      print('[WARN: ' + str(r.status_code) + '] ' + r.text)
      time.sleep(120)
    elif r.status_code != 200:
      print('[WARN: ' + str(r.status_code) + ':' + user_id + '] ' + r.text)
      return None
    else:
      return json.loads(r.text)
