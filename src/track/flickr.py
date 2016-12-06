#!/usr/bin/python3

import datetime
today = str(datetime.date.today())
since = int(datetime.datetime.strptime(today, '%Y-%m-%d').strftime("%s"))

api_key = "f84850c3a7c57d2a581ec6aad6eea5e9"

import people
persons = people.load('/vagrant/data/people.json.pretty')

import json
import flickr_api

for twitter_id, person in persons.items():
  if 'flickr' not in person:
    continue
  flickr = person['flickr']
  if 'id' not in flickr:
    print('[WARN][' + twitter_id + '] flickr id is missing')
    if 'username' not in flickr:
      print('[WARN][' + twitter_id + '] flickr user name is missing')
      continue
    username = flickr['username']
    body = flickr_api.people_findByUsername(api_key, username)
    remote_id = json.loads(body)
    flickr['id'] = remote_id['user']['nsid']
  id = flickr['id']
  if '_activity' not in flickr:
    flickr['_activity'] = {}
  activity = flickr['_activity']
  body = flickr_api.people_getPhotos(api_key, id, since)
  remote_photos = json.loads(body)
  activity[today] = {'photos':remote_photos['photos']['photo']}

people.save(persons, '/vagrant/data/people.json')
