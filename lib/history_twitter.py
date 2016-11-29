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
