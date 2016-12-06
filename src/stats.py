#!/usr/bin/python3

import datetime, json, re

import config, people, tweets, tips
import history, history_fitbit, history_foursquare, history_twitter
import foursquare_api, twitter_api

token = config.load_token('/vagrant/token/twitter.json')
token_foursquare = config.load_token('/vagrant/token/foursquare.json')

local_tweets = tweets.load('/vagrant/data/tweets.json.pretty')
local_tips = tips.load('/vagrant/data/tips.json.pretty')

from_date = '2016-01-01'
to_date = '2016-12-31'

weekdays = {
  'Mon': '1_Mon',
  'Tue': '2_Tue',
  'Wed': '3_Wed',
  'Thu': '4_Thu',
  'Fri': '5_Fri',
  'Sat': '6_Sat',
  'Sun': '7_Sun'
}

months = {
  'Jan': '01',
  'Feb': '02',
  'Mar': '03',
  'Apr': '04',
  'May': '05',
  'Jun': '06',
  'Jul': '07',
  'Aug': '08',
  'Sep': '09',
  'Oct': '10',
  'Nov': '11',
  'Dec': '12'
}

stats = {}

def twitter(entity):
  if '_activity' not in entity:
    return
  activity = history.matching_days(entity['_activity'], from_date, to_date)
  if len(activity) == 0:
    return

  _from = history.first(activity)
  _to = history.last(activity)
  statuses_count = history_twitter.statuses_count(activity)
  favourites_count = history_twitter.favourites_count(activity) 
  friends_count = history_twitter.friends_count(activity)

  photos = history_twitter.photos(activity)
  if '_' not in stats[id]:
    stats[id]['_'] = {}
  if 'photos' not in stats[id]['_']:
    stats[id]['_']['photos'] = []
  for photo, ignore in photos.items():
    stats[id]['_']['photos'].append(photo)
#  friends_since_count = history_twitter.friends_since_count(activity)

  weekday = {}
  hour = {}
  weekday_hour = {}
  for day, metrics in activity.items():
    if 'tweets' not in metrics:
      continue
    for tweet_id in metrics['tweets']:
      tweet = None
      if tweet_id in local_tweets:
        tweet = local_tweets[tweet_id]
      else:
        remote_tweet = twitter_api.tweet(token, tweet_id)
        if remote_tweet is None:
          continue
        tweet = remote_tweet
        local_tweets[tweet_id] = remote_tweet
        tweets.save(local_tweets, '/vagrant/data/tweets.json')
      #'Sun Sep 11 02:49:04 +0000 2016'
      m = re.search('^(.{3}) (.{3}) (.{2}) (.{2}):(.{2}):(.{2}) (.{5}) (.{4})$', tweet['created_at'])
      date = m.group(8) + '-' + months[m.group(2)] + '-' + m.group(3)
      if date >= from_date and date <= to_date:      
        # weekday
        if weekdays[m.group(1)] not in weekday:
          weekday[weekdays[m.group(1)]] = 1
        else:
          weekday[weekdays[m.group(1)]] += 1
        # hour
        if m.group(4) not in hour:
          hour[m.group(4)] = 1
        else:
          hour[m.group(4)] += 1
        # weekday/hour
        if weekdays[m.group(1)] + '-' + m.group(4) not in weekday_hour:
          weekday_hour[weekdays[m.group(1)] + '-' + m.group(4)] = 1
        else:
          weekday_hour[weekdays[m.group(1)] + '-' + m.group(4)] += 1

  stats[id]['twitter'] = {
    '_from':_from,
    '_to':_to,
    'count_statuses':statuses_count,
    'count_favourites':favourites_count,
    'count_friends':friends_count,
#    'count_friends_since':friends_since_count,
    'histogram__weekday':weekday,
    'histogram__hour':hour,
    'histogram_weekday_hour':weekday_hour
  }

def foursquare(entity):
  if '_activity' not in entity:
    return
  activity = history.matching_days(entity['_activity'], from_date, to_date)
  if len(activity) == 0:
    return

  _from = history.first(activity)
  _to = history.last(activity)
  tips_count = history_foursquare.tips_count(activity)
  checkins_count = history_foursquare.checkins_count(activity) 
  friends_count = history_foursquare.friends_count(activity)
  friends_since_count = history_foursquare.friends_since_count(activity)

  photos = history_foursquare.photos(activity)
  if '_' not in stats[id]:
    stats[id]['_'] = {}
  if 'photos' not in stats[id]['_']:
    stats[id]['_']['photos'] = []
  for photo, ignore in photos.items():
    stats[id]['_']['photos'].append(photo)

  weekday = {}
  hour = {}
  weekday_hour = {}
  for day, metrics in activity.items():
    if 'tips' not in metrics:
      continue
    for tip_id in metrics['tips']:
      if tip_id[0] == 't':
        tip_id = tip_id[1:]
      print(tip_id)
      tip = None
      if tip_id in local_tips:
        tip = local_tips[tip_id]
      elif 't' + tip_id in local_tips:
        tip = local_tips['t'+tip_id]
      else:
        remote_tip = foursquare_api.tip(token_foursquare, tip_id)
        if remote_tip is None:
          continue
        tip = remote_tip
        local_tips[tip_id] = remote_tip
        tips.save(local_tips, '/vagrant/data/tips.json')
      timestamp = tip['response']['tip']['createdAt']
      date = datetime.datetime.fromtimestamp(int(timestamp))
      Ymd = date.strftime('%Y-%m-%d')
      print(Ymd)
      if Ymd >= from_date and Ymd <= to_date:
        a = date.strftime('%a')
        H = date.strftime('%H')
        # weekday
        if weekdays[a] not in weekday:
          weekday[weekdays[a]] = 1
        else:
          weekday[weekdays[a]] += 1
        # hour
        if H not in hour:
          hour[H] = 1
        else:
          hour[H] += 1
        # weekday/hour
        if weekdays[a] + '-' + H not in weekday_hour:
          weekday_hour[weekdays[a] + '-' + H] = 1
        else:
          weekday_hour[weekdays[a] + '-' + H] += 1

  stats[id]['foursquare'] = {
    '_from':_from,
    '_to':_to,
    'count_tips':tips_count,
    'count_checkins':checkins_count,
    'count_friends':friends_count,
    'count_friends_since':friends_since_count,
    'histogram__weekday':weekday,
    'histogram__hour':hour,
    'histogram_weekday_hour':weekday_hour
  }

def fitbit(entity):
  if '_activity' not in entity:
    return
  activity = history.matching_days(entity['_activity'], from_date, to_date)
  if len(activity) == 0:
    return

  _from = history.first(activity)
  _to = history.last(activity)
  distance = history_fitbit.distance(activity)
  floors = history_fitbit.floors(activity)
  steps = history_fitbit.steps(activity)
  stats[id]['fitbit'] = {
    '_from':_from,
    '_to':_to,
    'distance':distance,
    'floors':floors,
    'steps':steps
  }

def profile():
  most_active_in = 'twitter'
  keys1 = sorted(stats[id]['foursquare']['count_checkins'])
  keys2 = sorted(stats[id]['twitter']['count_statuses'])
  if stats[id]['foursquare']['count_checkins'][keys1[-1]] > stats[id]['twitter']['count_statuses'][keys2[-1]]:
    most_active_in = 'foursquare'
  
  more_friends_in = 'twitter'
  keys1 = sorted(stats[id]['foursquare']['count_friends'])
  keys2 = sorted(stats[id]['twitter']['count_friends'])
  if stats[id]['foursquare']['count_friends'][keys1[-1]] > stats[id]['twitter']['count_friends'][keys2[-1]]:
    more_friends_in = 'foursquare'

  if '_' not in stats[id]:
    stats[id]['_'] = {}
  stats[id]['_']['most-active-in'] = most_active_in
  stats[id]['_']['more-friends-in'] = more_friends_in

persons = people.load('/vagrant/data/people.json.pretty')

for id, person in persons.items():
  stats[id] = {}
  twitter(person['twitter'])
  foursquare(person['foursquare'])
  fitbit(person['fitbit'])
  profile()

with open('/vagrant/data/stats.json', 'w') as file:
  json.dump(stats, file, sort_keys=True)
