#!/usr/bin/python3

import datetime
today = str(datetime.date.today())

import people
persons = people.load('/vagrant/data/people.json')

import json, requests
from pyquery import PyQuery

for twitter_id, person in persons.items():
  if 'fitbit' not in person:
    continue
  fitbit = person['fitbit']
  if 'url' not in fitbit:
    print('[WARN][' + twitter_id + '] fitbit url is missing')
    continue
  url = fitbit['url']

  r = requests.get(url)

  pq = PyQuery(r.text)

  height = pq('li.user-stat.height')
  location = pq('li.user-stat.location')
  joined = pq('li.user-stat.location')

  aboutme = pq('div.content.firstContent')

  lifetime = pq('div.tabsData.lifetime.cached')
  lifetime_steps = lifetime('div.tabsData.steps')
  lifetime_floor = lifetime('div.tabsData.floor')
  lifetime_distance = lifetime('div.tabsData.distance')

  #best = pq('div.tabsData.bestStats.cached')
  best = pq('div#achievementsBest')
  best_steps = best('div.tabsData.steps')
  best_floor = best('div.tabsData.floor')
  best_distance = best('div.tabsData.distance')

  if '_activity' not in fitbit:
    fitbit['_activity'] = {}
  activity = fitbit['_activity']
  activity[today] = {
    'height':height.text(),
    'location':location.text(),
    'joined':joined.text(),
    'aboutme':aboutme.text(),
    'steps-all':lifetime_steps('span.value').text(),
    'floor-all':lifetime_floor('span.value').text(),
    'distance-all':lifetime_distance('span.value').text(),
    'steps-best':best_steps('span.value').text(),
    'floor-best':best_floor('span.value').text(),
    'distance-best':best_distance('span.value').text()
  }

people.save(persons, '/vagrant/data/people.json')
