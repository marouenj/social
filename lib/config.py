import json, sys

def load_token(path):
  # load
  with open(path) as file:
    token = json.load(file)

  # validate
  if 'token' not in token:
    print('[ERR] Json file not valid')
    sys.exit(1)

  return token['token']
