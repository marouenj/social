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
        match = re.match('^.*youtube\.com/watch\?v=.*$', url['expanded_url'])
        if not match:
          match = re.match('^.*youtube\.com/(.*/)*(.*)$', url['expanded_url'])
          if match:
            user['youtube'] = {'id':match.group(2)}

people.save(users, './people.json')
