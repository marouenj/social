def statuses_count(activity):
  keys = sorted(activity)
  first = keys[0]
  last = keys[-1]
  return activity[last]['statuses_count'] - activity[first]['statuses_count']

def favourites_count(activity):
  keys = sorted(activity)
  first = keys[0]
  last = keys[-1]
  return activity[last]['favourites_count'] - activity[first]['favourites_count']

def friends_count(activity):
  keys = sorted(activity)
  last = keys[-1]
  if 'friends_count' not in activity[last]:
    return None
  return activity[last]['friends_count']

def friends_since_count(activity):
  keys = sorted(activity)
  first = keys[0]
  last = keys[-1]
  if 'friends_count' not in activity[last] or 'friends_count' not in activity[first]:
    return None
  return activity[last]['friends_count'] - activity[first]['friends_count']
