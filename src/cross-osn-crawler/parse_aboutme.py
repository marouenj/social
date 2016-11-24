#!/usr/bin/python3

import requests
from pyquery import PyQuery

import people

users = people.load('./people.json.pretty')

i = 0
for k, user in users.items():
  if 'aboutme' not in user:
    continue

  i += 1
  print(str(i) + '/ user: ' + k)

  user_name = user['aboutme']['id']
  url = 'http://about.me/' + user_name

  r = requests.get(url)

  pq = PyQuery(r.text)
  links = pq('a.social-link')

  hrefs = []
  for link in links:
    hrefs.append(link.attrib['href'])

  hrefs.sort()
  user['aboutme']['social_links'] = hrefs

people.save(users, './people.json')
