#!/usr/bin/python3

import json, re

import config, people, tweets
import history, history_foursquare, history_twitter
import twitter_api

token = config.load_token('/vagrant/token/twitter.json')

local_tweets = tweets.load('./tweets.json')

from_date = '2016-11-17'
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
        tweets.save(local_tweets, './tweets.json')
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

  stats[id]['foursquare'] = {
    '_from':_from,
    '_to':_to,
    'count_tips':tips_count,
    'count_checkins':checkins_count,
    'count_friends':friends_count,
#    'count_friends_since':friends_since_count
  }

persons = people.load('./people.json.pretty')

i = 0
for id, person in persons.items():
  i += 1
  if i > 1:
    break
  print(i)
  stats[id] = {}
  twitter(person['twitter'])
  foursquare(person['foursquare'])
  
with open('./stats.json', 'w') as file:
  json.dump(stats, file, sort_keys=True)
