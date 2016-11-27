#!/usr/bin/python3

import datetime
#import json

import config, people, foursquare_api

token = config.load_token('/vagrant/token/foursquare.json')

users = people.load('./people.json.pretty')

today = str(datetime.date.today())

i = 0
for k, user in users.items():
  i += 1

  if i > 1:
    break

  print(i)
  foursquare = user['foursquare']
  if 'id' not in foursquare:
    continue
  user_id = foursquare['id']
  if user_id is None:
    continue

  remote_user = foursquare_api.user(token, user_id)
  if remote_user is None:
    continue
  #with open('./user.json', 'w') as file:
  #  json.dump(remote_user, file, sort_keys=True)

  #remote = foursquare_api.user_mayorships(token, user_id)
  #if remote is None:
  #  continue
  #with open('./mayorships.json', 'w') as file:
  #  json.dump(remote, file, sort_keys=True)

  #remote = foursquare_api.user_venuelikes(token, user_id)
  #if remote is None:
  #  continue
  #with open('./venuelikes.json', 'w') as file:
  #  json.dump(remote, file, sort_keys=True)

  #remote_tips = foursquare_api.user_tips(token, user_id)
  #if remote_tips is None:
  #  continue
  #with open('./tips.json', 'w') as file:
  #  json.dump(remote_tips, file, sort_keys=True)

  if '_activity' not in foursquare:
    foursquare['_activity'] = {}

  remote_user = remote_user['response']['user']

  tips = []

  delta_tips_count = foursquare_api.parse_delta_tips_count(foursquare, remote_user)
  if delta_tips_count > 0:
    remote_tips = foursquare_api.user_tips(token, user_id, count)
    if remote_tips is not None:
      remote_tips = remote_tips['response']['list']['listItems']['items']
      for tip in remote_tips:
        tips.append(tip['id'])

  activity = {
    'bio':remote_user['bio'],
    'friends_count':remote_user['friends']['count'],
    'tips_count':remote_user['tips']['count'],
    'checkins_count':remote_user['checkins']['count'],
    'lists_count':remote_user['lists']['count'],
    'mayorships_count':remote_user['mayorships']['count'],
    'todo_count':foursquare_api.parse_todo_count(remote_user),
    'venuelikes_count':foursquare_api.parse_venuelikes_count(remote_user),
    'tips':tips
  }

  foursquare['_activity'][today] = activity
  foursquare['_last_activity'] = today

people.save(users, './people.json')
