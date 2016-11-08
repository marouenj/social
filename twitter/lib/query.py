import json, os, sys

# keys in json file
i = 'id'
q = 'q'

def load_queries(path):
  # load
  with open(path) as queries_file:
    queries = json.load(queries_file)

  for query in queries:
    # validate query
    if i not in query or q not in query:
      print('[ERR] Json file not valid')
      sys.exit(1)

  return queries

def init_queries_output_file(queries, base):
  for query in queries:
    oput = query[i] + '.json'
    path = base + '/' + oput
    if not os.path.exists(path):
      with open(path, 'w') as tweets_file:
        tweets = {'since_id': '0', 'tweets': []}
        json.dump(tweets, tweets_file)
        tweets_file.close()

# request params
count = 100
