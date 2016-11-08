import json, sys

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

def load_access_token(path):
  # load
  with open(path) as access_token_file:
    access_token = json.load(access_token_file)

  # key in json file
  access_token_key = 'access_token'

  # validate
  if access_token_key not in access_token:
    print('[ERR] Json file not valid')
    sys.exit(1)

  return access_token[access_token_key]
