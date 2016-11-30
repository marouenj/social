import json, os

# create a tip db from scratch
def init(path):
  if not os.path.exists(path):
    tips = {}
    file = open(path, 'w')
    json.dump(tips, file, sort_keys=True)
    file.close()

def load(path):
  init(path)
  with open(path) as file:
    tips = json.load(file)
  return tips 

def save(tips, path):
  with open(path, 'w') as file:
    json.dump(tips, file, sort_keys=True)
