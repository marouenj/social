def matching_days(activity, from_date, to_date):
  return {k:v for k, v in activity.items() if k >= from_date and k <= to_date}

def test_matching_days():
  activity = {'2016-11-10':{}, '2016-11-20':{}}

  days = matching_days(activity, '2016-11-10', '2016-11-20')
  if len(days) == 2:
    print('YES')
  else:
    print('NO')

  days = matching_days(activity, '2016-11-15', '2016-11-20')
  if len(days) == 1:
    print('YES')
  else:
    print('NO')

  days = matching_days(activity, '2016-11-10', '2016-11-15')
  if len(days) == 1:
    print('YES')
  else:
    print('NO')

def first(activity):
  keys = sorted(activity)
  return keys[0]

def last(activity):
  keys = sorted(activity)
  return keys[-1]

