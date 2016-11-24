#!/usr/bin/python3

import datetime
import config, people, instagram_api
import json

token = config.load_token('/vagrant/token/instagram.json')

users = people.load('./people.json.pretty')

today = datetime.date.today()

i = 0
for user_id, user in users.items():
  i += 1
  if i > 4:
    break
  print(i)
  instagram = user['instagram']
  if 'id' not in instagram:
    continue
  user_id = instagram['id']
  if user_id is None:
    continue
  print(user_id)
  user_media = instagram_api.user_media(token, user_id)
  if user_media is not None:
    if '_activity' not in instagram:
      instagram['_activity'] = {}
#    activity = {'statuses_count':remote_user['statuses_count'],'favourites_count':remote_user['favourites_count'],'friends_count':remote_user['friends_count'],'followers_count':remote_user['followers_count'],'listed_count':remote_user['listed_count']}
    instagram['_activity'][str(today)] = activity

  with open('./user_media.json', 'w') as file:
    json.dump(user_media, file, sort_keys=True)

#people.save(users, './people.json')
