#!/usr/bin/python3

import re
import people

users = people.load('./people.json')

for user_id, user in users.items():
  if 'entities' in user['twitter']:
    entities = user['twitter']['entities']
    urls = []
    if 'description' in entities:
      urls.extend(entities['description']['urls'])
    if 'url' in entities:
      urls.extend(entities['url']['urls'])
    for url in urls:
      if 'expanded_url' in url and url['expanded_url'] is not None:
        match = re.match('^.*about\.me/(.*)$', url['expanded_url'])
        if match:
          user['aboutme'] = {'id':match.group(1)}

people.save(users, './people.json')
