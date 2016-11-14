#!/usr/bin/python3

# https://dev.twitter.com/rest/public/search
# https://dev.twitter.com/rest/reference/get/search/tweets

import json
import os.path
import requests
import sys

import auth
import query

from query import i, q, count

# path
access_token_path = './2config/access_token.json'

# load access token
access_token = auth.load_access_token(access_token_path)

# paths
search_queries = './2config/search_queries.json'
data_dir = './3data'

# load queries
queries = query.load_queries(search_queries)
query.init_queries_output_file(queries, data_dir)

# execute each query
for query in queries:
  path = data_dir + '/' + query[i] + '.json'

  # load previously saved tweets from the same query
  with open(path, 'r+') as tweets_file:
    tweets = json.load(tweets_file)

  # request
  url = 'https://api.twitter.com/1.1/search/tweets.json'
  params = {'q': query[q], 'result_type': 'recent', 'count': count, 'since_id': tweets['since_id']}
  headers= {'Authorization': 'Bearer ' + access_token}
  r = requests.get(url, params=params, headers=headers)

  # check response status
  if r.status_code is 429:
    print('[WARN] Too many request')
    sys.exit(429)
  if r.status_code is not 200:
    print('[ERR] Failure to get tweets')
    print(r.status_code)
    print(r.text)
    sys.exit(1)

  # convert string to json structure
  tweets_remote = json.loads(r.text)
  print('[INFO] Retrieved ' + str(len(tweets_remote['statuses'])) + ' tweets')

  # update since_id
  tweets['since_id'] = tweets_remote['search_metadata']['max_id_str']

  # discard already existing
  new_tweets = [tweet for tweet in tweets_remote['statuses'] if tweet['id_str'] not in tweets['tweets_idx']]
  print('[INFO] Discarded ' + str(len(tweets_remote['statuses']) - len(new_tweets)) + ' tweets')

  for tweet in new_tweets:
    # index for fast lookup
    tweets['tweets_idx'].append(tweet['id_str'])
    # del
    for key in [
    'contributors',
    'coordinates',
    'favorite_count',
    'favorited',
    'geo',
    'id',
    'in_reply_to_screen_name',
    'in_reply_to_status_id',
    'in_reply_to_status_id_str',
    'in_reply_to_user_id',
    'in_reply_to_user_id_str',
    'is_quote_status',
    'possibly_sensitive',
    'retweet_count',
    'retweeted'
    ]:
      if key in tweet:
        del tweet[key]
    for key in [
    'contributors_enabled',
    'default_profile',
    'default_profile_image',
    'favourites_count',
    'follow_request_sent',
    'followers_count',
    'following',
    'friends_count',
    'geo_enabled',
    'has_extended_profile',
    'id',
    'is_translation_enabled',
    'is_translator',
    'listed_count',
    'notifications',
    'profile_background_color',
    'profile_background_image_url',
    'profile_background_image_url_https',
    'profile_background_tile',
    'profile_image_url',
    'profile_image_url_https',
    'profile_link_color',
    'profile_sidebar_border_color',
    'profile_sidebar_fill_color',
    'profile_text_color',
    'profile_use_background_image',
    'statuses_count',
    'translator_type'
    ]:
      if key in tweet['user']:
        del tweet['user'][key]

    # append
    tweets['tweets'].append(tweet)

  with open(path, 'w') as tweets_file:
    json.dump(tweets, tweets_file, sort_keys=True)

print('[INFO] Success')
