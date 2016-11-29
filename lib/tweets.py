import json, os

# create a tweet db from scratch
def init(path):
  if not os.path.exists(path):
    tweets = {}
    file = open(path, 'w')
    json.dump(tweets, file, sort_keys=True)
    file.close()

def load(path):
  init(path)
  with open(path) as file:
    tweets = json.load(file)
  return tweets 

def save(tweets, path):
  with open(path, 'w') as file:
    json.dump(tweets, file, sort_keys=True)
