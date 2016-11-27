#!/usr/bin/python3

import datetime
import config, people, twitter_api

token = config.load_token('/vagrant/token/twitter.json')

users = people.load('./people.json.pretty')

today = datetime.date.today()

i = 0
for user_id, user in users.items():
  i += 1
  print(i)

  u = twitter_api.user(token, user_id)
  if u is None:
    continue

  if 'since_id' not in user['twitter']:
    user['twitter']['since_id'] = -1
  since_id = user['twitter']['since_id']

  ids = twitter_api.user_tweets_id(token, user_id, since_id)

  if '_activity' not in user['twitter']:
    user['twitter']['_activity'] = {}

  activity = {
  'statuses_count':u['statuses_count'],
  'favourites_count':u['favourites_count'],
  'friends_count':u['friends_count'],
  'followers_count':u['followers_count'],
  'listed_count':u['listed_count'],
  'tweets':ids
  }
  user['twitter']['_activity'][str(today)] = activity

  if (len(ids) > 0):
    user['twitter']['since_id'] = ids[-1]

people.save(users, './people.json')
