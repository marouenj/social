#!/usr/bin/python3

import json, re

import config, people, tweets
import history, history_foursquare, history_twitter
import twitter_api

token = config.load_token('/vagrant/token/twitter.json')

from_date = '2016-01-01'
to_date = '2016-12-31'

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

  created_at = []
  for day, metrics in activity.items():
    if 'tweets' not in metrics:
      continue
    for tweet_id in metrics['tweets']:
      local_tweets = tweets.load('./tweets.json')
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
      created_at.append(m.group(8) + '-' + m.group(2) + '-' + m.group(3) + '-' + m.group(1) + '-' + m.group(4))

  stats[id]['twitter'] = {
    '_from':_from,
    '_to':_to,
    'statuses_count':statuses_count,
    'favourites_count':favourites_count,
    'created_at':created_at
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

  stats[id]['foursquare'] = {
    '_from':_from,
    '_to':_to,
    'tips_count':tips_count,
    'checkins_count':checkins_count
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
  
with open('./stats_' + from_date + '_' + to_date + '.json', 'w') as file:
  json.dump(stats, file, sort_keys=True)
