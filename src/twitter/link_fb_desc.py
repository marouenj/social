#!/usr/bin/python3

import jellyfish, json, os, re

import people
from url import expand

# work dir
work_dir = os.environ['WORKDIR']
twitter_dir = os.environ['TWITTERDIR']

# load people
people_path = work_dir + '/data/people.json'
persons = people.load(people_path)

# load tweets
tweets_path = twitter_dir + '/3data/url_facebook.json'
with open(tweets_path, 'r') as tweets_file:
  tweets = json.load(tweets_file)

# for each tweet
i = 0
for tweet in tweets['tweets']:
  i+=1

  user = tweet['user']
  tw_name = user['name']
  tw_username = user['screen_name']
  urls = user['entities']['description']['urls']

  # for each url
  for url in urls:
    expanded_url = url['expanded_url']
    try:
      expanded_url = expand(expanded_url)
    except:
      print('[WARN] @' + str(i) + ' Url not valid')
      continue
    url_match = re.match('^.*facebook\.com/(.*)$', expanded_url)
    if url_match:
      fb_username = url_match.group(1)
      person = {'twitter':{'name':tw_name, 'screen_name':tw_username}, 'facebook':{'username':fb_username}, '_':{'tw_fb_jaro':jellyfish.jaro_distance(tw_username, fb_username)}}
      people.link_tw_fb(person, persons)
      continue

people.save(persons, people_path)

print('[INFO] Success')