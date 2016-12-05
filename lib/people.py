import codecs, json, os

# create a people db from scratch
def init(path):
  if not os.path.exists(path):
    persons = {}
    save(persons, path)

def load(path):
  init(path)
  with codecs.open(path, 'r', 'utf-8') as file:
    persons = json.load(file)
  return persons

def save(persons, path):
  with codecs.open(path, 'w', 'utf-8') as file:
    json.dump(persons, file, sort_keys=True, ensure_ascii=False)
