import json
import sys

# keys in json file
key = 'consumer_key'
secret = 'consumer_secret'

def load_credentials(path):
  # load
  with open(path) as credentials_file:
    credentials = json.load(credentials_file)

  # validate
  if key not in credentials or secret not in credentials:
    print('[ERR] Json file not valid')
    sys.exit(1)

  return credentials
