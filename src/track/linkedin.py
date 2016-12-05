#!/usr/bin/python3

import datetime
today = str(datetime.date.today())

import people
persons = people.load('/vagrant/data/people.json.pretty')

import json, requests
from pyquery import PyQuery

for twitter_id, person in persons.items():
  if 'linkedin' not in person:
    continue
  linkedin = person['linkedin']
  if 'url' not in linkedin:
    print('[WARN][' + twitter_id + '] linkedin url is missing')
    continue
  url = linkedin['url']

  url = 'https://pinterest.com/larryconlin'

  r = requests.get(url)

  with open('/tmp/index.html', 'w') as file:
    file.write(r.text)

  pq = PyQuery(r.text)

  div = pq('div.profile-picture')
  print(div.text())
  link = pq('a.photo')
  url_photo = link.attrib['href']

  if '_activity' not in linkedin:
    linkedin['_activity'] = {}
  activity = linkedin['_activity']
  activity[today] = {
    'url-photo': url_photo
  }

people.save(persons, '/vagrant/data/people.json')
