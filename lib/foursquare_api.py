import json, requests, time

def get(url, params, user_id):
  while True:
    r = requests.get(url, params=params)
    if r.status_code == 403:
      print('[WARN: ' + str(r.status_code) + '] ' + r.text)
      time.sleep(120)
    elif r.status_code != 200:
      print('[WARN: ' + str(r.status_code) + ':' + user_id + '] ' + r.text)
      return None
    else:
      return json.loads(r.text)

def user(token, user_id):
  url = 'https://api.foursquare.com/v2/users/' + user_id
  params = {'oauth_token': token, 'v':'20161116'}
  return get(url, params, user_id)

# only self can be used as user_id for now
def user_checkins(token, user_id):
  url = 'https://api.foursquare.com/v2/users/' + user_id + '/checkins'
  params = {'oauth_token': token, 'limit':'250', 'sort':'newestfirst', 'v':'20161116'}
  return get(url, params, user_id)

def user_mayorships(token, user_id):
  url = 'https://api.foursquare.com/v2/users/' + user_id + '/mayorships'
  params = {'oauth_token': token, 'v':'20161116'}
  return get(url, params, user_id)

def user_venuelikes(token, user_id):
  url = 'https://api.foursquare.com/v2/users/' + user_id + '/venuelikes'
  params = {'oauth_token': token, 'limit':'100', 'v':'20161116'}
  return get(url, params, user_id)

def user_tips(token, user_id, count):
  url = 'https://api.foursquare.com/v2/lists/' + user_id + '/tips'
  params = {'oauth_token': token, 'limit':count, 'sort':'recent', 'v':'20161116'}
  return get(url, params, user_id)

# returns 404
def user_tastes(token, user_id):
  url = 'https://api.foursquare.com/v2/users/' + user_id + '/tastes'
  params = {'oauth_token': token, 'v':'20161116'}
  return get(url, params, user_id)

def tip(token, tip_id):
  url = 'https://api.foursquare.com/v2/tips/' + tip_id
  params = {'oauth_token': token, 'v':'20161116'}
  return get(url, params, tip_id)

def parse_todo_count(user):
  groups = user['lists']['groups']
  for group in groups:
    if group['type'] == 'yours':
      for item in group['items']:
        if item['type'] == 'todos':
          return item['listItems']['count']
  return None

def parse_venuelikes_count(user):
  groups = user['lists']['groups']
  for group in groups:
    if group['type'] == 'yours':
      for item in group['items']:
        if item['type'] == 'likes':
          return item['listItems']['count']
  return None

def parse_delta_tips_count(user, remote_user):
  if '_last_activity' in user:
    last_tip_count = user['_activity'][user['_last_activity']]['tips_count']
    curr_tip_count = remote_user['tips']['count']
    return curr_tip_count - last_tip_count
  return 0
