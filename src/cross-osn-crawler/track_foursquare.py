#!/usr/bin/python3

import datetime
import config, people, foursquare_api

token = config.load_token('/vagrant/token/foursquare.json')

users = people.load('./people.json.pretty')

today = str(datetime.date.today())

i = 0
for k, user in users.items():
  i += 1
  print(i)
  foursquare = user['foursquare']
  if 'id' not in foursquare:
    continue
  user_id = foursquare['id']
  if user_id is None:
    continue
  remote_user = fsq_api.user(token, user_id)
  if remote_user is None:
    continue
  if '_activity' not in foursquare:
    foursquare['_activity'] = {}
  remote_user = remote_user['response']['user']
  activity = {'friends_count':remote_user['friends']['count'],'tips_count':remote_user['tips']['count'],'checkins_count':remote_user['checkins']['count']}
  foursquare['_activity'][today] = activity

people.save(users, './people.json')
