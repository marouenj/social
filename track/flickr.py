#!/usr/bin/python3

import flickr_api

api_key = "e09976a29c631784a9ca937bc494cb96"
user_id = ""

resp = flickr_api.people_info(api_key, user_id)
print(resp.text)
