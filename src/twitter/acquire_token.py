#!/usr/bin/python3

# https://dev.twitter.com/oauth/application-only

import json
import requests
import sys

from auth import load_credentials, key, secret

# path
iput_path = './2config/credentials.json'
oput_path = './2config/access_token.json'

# load
credentials = load_credentials(iput_path)

# request
url = 'https://api.twitter.com/oauth2/token'
auth = (credentials[key], credentials[secret])
data = {'grant_type' : 'client_credentials'}
r = requests.post(url, auth=auth, data=data)

# check response status
if r.status_code is not 200:
  print('[ERR] Failure to acquire access token')
  sys.exit(1)

# convert string to json structure
access_token = json.loads(r.text)

# delete unnecessary keys
del access_token['token_type']

# open output file (override)
with open(oput_path, 'w') as access_token_file:
    json.dump(access_token, access_token_file)

print('[INFO] Success')
