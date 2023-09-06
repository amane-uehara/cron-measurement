from datetime import datetime, timedelta

def time_list(start_yyyymmdd, end_yyyymmdd, increment_second):
  start_time = datetime.strptime(start_yyyymmdd, "%Y%m%d%H%M%S")
  end_time   = datetime.strptime(end_yyyymmdd, "%Y%m%d%H%M%S")
  increment  = timedelta(seconds=int(increment_second))

  ret = []
  current_time = start_time
  while current_time <= end_time:
    ret.append(current_time.strftime("%Y%m%d%H%M%S"))
    current_time += increment

  print(ret)
  return ret
