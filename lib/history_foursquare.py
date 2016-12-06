def tips_count(activity):
  count = {}
  for k, metrics in activity.items():
    count[k] = metrics['tips_count']
  return count
#  keys = sorted(activity)
#  first = keys[0]
#  last = keys[-1]
#  if 'tips_count' not in activity[last] or 'tips_count' not in activity[first]:
#    return None
#  return activity[last]['tips_count'] - activity[first]['tips_count']

def checkins_count(activity):
  count = {}
  for k, metrics in activity.items():
    count[k] = metrics['checkins_count']
  return count
#  keys = sorted(activity)
#  first = keys[0]
#  last = keys[-1]
#  if 'checkins_count' not in activity[last] or 'checkins_count' not in activity[first]:
#    return None
#  return activity[last]['checkins_count'] - activity[first]['checkins_count']

def friends_count(activity):
  count = {}
  for k, metrics in activity.items():
    count[k] = metrics['friends_count']
  return count
#  keys = sorted(activity)
#  last = keys[-1]
#  if 'friends_count' not in activity[last]:
#    return None
#  return activity[last]['friends_count']

def friends_since_count(activity):
  keys = sorted(activity)
  first = keys[0]
  last = keys[-1]
  if 'friends_count' not in activity[last] or 'friends_count' not in activity[first]:
    return None
  return activity[last]['friends_count'] - activity[first]['friends_count']

def photos(activity):
  photos = {}
  for k, metrics in activity.items():
    photos[metrics['photo']['prefix'] + '100x100' + metrics['photo']['suffix']] = None
  return photos
