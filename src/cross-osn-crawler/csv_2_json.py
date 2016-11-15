#!/usr/bin/python3

import csv
import people

users = people.load('./people.json')

with open('./osn-data/users_linked.csv', newline='') as file:
  csv_reader = csv.reader(file, delimiter=',')
  for row in csv_reader:
    if row[0] in users:
      print('[WARN] User ' + row[0] + ' exists')
    else:
      user = {'twitter':{'id':row[0]},'instagram':{'id':row[1]},'foursquare':{'id':row[2]}}
      users[row[0]] = user

people.save(users, './people.json')
