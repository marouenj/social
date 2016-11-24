#!/usr/bin/python3

import csv, json, requests, sys

import people

def load_access_token(path='./access_token.json'):
  # load
  with open(path) as access_token_file:
    access_token = json.load(access_token_file)

  # key in json file
  access_token_key = 'access_token'

  # validate
  if access_token_key not in access_token:
    print('[ERR] Json file not valid')
    sys.exit(1)

  return access_token[access_token_key]

def twitter_api_users_show(user_id, access_token):
  url = 'https://api.twitter.com/1.1/users/show.json'
  params = {'user_id': user_id, 'include_entities': 'true'}
  headers= {'Authorization': 'Bearer ' + access_token}

  while True:
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 429:
      print('[WARN: ' + str(r.status_code) + '] Too many request')
      time.sleep(120)
    elif r.status_code != 200:
      print('[WARN: ' + str(r.status_code) + ':' + user_id + '] ' + r.text)
      return None
    else:
      return json.loads(r.text)

access_token = load_access_token()

users = people.load('./people.json')

for user_id, user in users.items():
  remote_user = twitter_api_users_show(user_id, access_token)
  if remote_user is not None:
    user['twitter']['screen_name'] = remote_user['screen_name']
    user['twitter']['entities'] = remote_user['entities']

people.save(users, './people.json')
