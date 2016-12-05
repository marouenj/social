#!/usr/bin/python3

import json, os.path, requests, sys

import config
token = config.load_token('/vagrant/token/twitter.json')

# load queries
import query
from query import i, q, count
queries = query.load_queries('/vagrant/data/twitter_search_queries.json')
query.init_queries_output_file(queries, '/vagrant/data')

# execute each query
for query in queries:
  path = '/vagrant/data/' + query[i] + '.json'

  # load previously saved tweets from the same query
  with open(path, 'r+') as tweets_file:
    tweets = json.load(tweets_file)

  # request
  url = 'https://api.twitter.com/1.1/search/tweets.json'
  params = {'q': query[q], 'result_type': 'recent', 'count': count, 'since_id': tweets['since_id']}
  headers= {'Authorization': 'Bearer ' + token}
  r = requests.get(url, params=params, headers=headers)

  # check response status
  if r.status_code is not 200:
    print('[ERR] ' + r.text)
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

    # append
    tweets['tweets'].append(tweet)

  with open(path, 'w') as tweets_file:
    json.dump(tweets, tweets_file, sort_keys=True)

print('[INFO] Success')
