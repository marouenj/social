def distance(activity):
  count = {}
  for k, metrics in activity.items():
    count[k] = metrics['distance-all']
  return count

def floors(activity):
  count = {}
  for k, metrics in activity.items():
    count[k] = metrics['floor-all']
  return count

def steps(activity):
  count = {}
  for k, metrics in activity.items():
    count[k] = metrics['steps-all']
  return count
