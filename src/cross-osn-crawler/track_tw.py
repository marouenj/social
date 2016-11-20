#!/usr/bin/python3

import datetime
import people, tw_api, tw_auth

access_token = tw_auth.load_access_token('./access_token.json')

users = people.load('./people.json.pretty')

today = datetime.date.today()

i = 0
for user_id, user in users.items():
  i += 1
  print(i)
  remote_user = tw_api.users_show(access_token, user_id)
  if remote_user is not None:
    if '_activity' not in user['twitter']:
      user['twitter']['_activity'] = {}
    activity = {'statuses_count':remote_user['statuses_count'],'favourites_count':remote_user['favourites_count'],'friends_count':remote_user['friends_count'],'followers_count':remote_user['followers_count'],'listed_count':remote_user['listed_count']}
    user['twitter']['_activity'][str(today)] = activity

people.save(users, './people.json')
