import json, os

# create a people db from scratch
def init(path):
  if not os.path.exists(path):
    persons = {}
    file = open(path, 'w')
    json.dump(persons, file, sort_keys=True)
    file.close()

def load(path):
  init(path)
  with open(path) as file:
    persons = json.load(file)
  return persons

def save(persons, path):
  with open(path, 'w') as file:
    json.dump(persons, file, sort_keys=True)

def link_tw_fb(person, persons):
  screen_name = person['twitter']['screen_name']
  if screen_name in persons:
    print('[INFO] Updating ' + screen_name)
    existing_person = persons[screen_name]
    if 'tw_fb_jaro' in existing_person['_']:
      if person['_']['tw_fb_jaro'] > existing_person['_']['tw_fb_jaro']:
        print('  [INFO] Higher \'_\'.\'tw_fb_jaro\'')
        existing_person['_']['tw_fb_jaro'] = person['_']['tw_fb_jaro']
        existing_person['facebook']['username'] = person['facebook']['username']
        # delete other keys since they refer to another account
    else:
      print('  [INFO] Linking')
      existing_person['_']['tw_fb_jaro'] = person['_']['tw_fb_jaro']
      existing_person['facebook']['username'] = person['facebook']['username']
  else:
    print('[INFO] Creating ' + screen_name)
    print('  [INFO] Linking')
    persons[screen_name] = person