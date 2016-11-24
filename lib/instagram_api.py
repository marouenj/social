import json, requests, time

def user_media(token, user_id):
  url = 'https://api.instagram.com/v1/users/' + user_id + '/media/recent/'
  params = {'access_token': token, 'count':'10'}

  while True:
    r = requests.get(url, params=params)
    if r.status_code == 429:
      print('[WARN: ' + str(r.status_code) + '] ' + r.text)
      time.sleep(120)
    elif r.status_code != 200:
      print('[WARN: ' + str(r.status_code) + ':' + user_id + '] ' + r.text)
      return None
    else:
      return json.loads(r.text)
