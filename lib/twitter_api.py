import json, requests, time
from requests.exceptions import ConnectionError, SSLError

def twitter_get_request(user_id, url, params, headers):
  while True:
    try:
      r = requests.get(url, params=params, headers=headers)
    except ConnectionError:
      print('[WARN] Connection Error')
      continue
    except SSLError:
      print('[WARN] SSL Error')
      continue
    if r.status_code == 429:
      print('[WARN: ' + str(r.status_code) + '] ' + r.text)
      time.sleep(120)
    elif r.status_code != 200:
      print('[WARN: ' + str(r.status_code) + ':' + user_id + '] ' + r.text)
      return None
    else:
      return json.loads(r.text)

def user(token, user_id):
  url = 'https://api.twitter.com/1.1/users/show.json'
  params = {'user_id': user_id, 'include_entities': 'true'}
  headers= {'Authorization': 'Bearer ' + token}
  return twitter_get_request(user_id, url, params, headers)

def user_tweets(token, user_id, since_id):
  url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
  params = {'user_id':user_id,'trim_user':'true','exclude_replies':'true'}
  if since_id != -1:
    params['since_id'] = since_id
  headers= {'Authorization': 'Bearer ' + token}
  return twitter_get_request(user_id, url, params, headers)

def user_tweets_id(token, user_id, since_id):
  tweets = user_tweets(token, user_id, since_id)
  ids = []
  if tweets is not None:
    for tweet in tweets:
      ids.append(tweet['id_str'])
  ids.sort()
  return ids
