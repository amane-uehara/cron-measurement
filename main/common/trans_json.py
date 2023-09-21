import sys
import json
from math import floor
from datetime import datetime, timedelta

def search_read(key_str, data_dict):
  key_list = key_str.split(".")
  key = key_list.pop(0)

  if key not in data_dict:
    return ""
  elif len(key_list) == 0:
    return data_dict[key]
  elif len(key_list) >= 1:
    return search_read(".".join(key_list), data_dict[key])

def search_write(key_str, value, data_dict):
  if not isinstance(data_dict, dict):
    return {}

  key_list = key_str.split(".")
  ret = data_dict.copy()

  tmp = ret
  while len(key_list) >= 2:
    key = key_list.pop(0)
    if key not in tmp:
      tmp[key] = {}
    tmp = tmp[key]

  tmp[key_list[0]] = value
  return ret

def default_run_key_list():
  return [
    "dt",
    "yyyymmdd",
    "hh",
    "hostname",
    "mac_addr",
    "sensor_mac_addr",
    "sensor_location"
  ]

def trans_to_list_list(json_list, config, default_data_key_list):
  key_list = join_run_data_key_list(default_run_key_list(), default_data_key_list, config)

  ret = []
  for run in json_list:
    tmp = []
    for dot_key in key_list:
      tmp.append(search_read(dot_key, run))
    ret.append(tmp)

  return ret

def trans_to_selected_json_list(json_list, config):
  if "key_dict" in config:
    key_dict = config["key_dict"]
  else:
    print("ERROR: key_dict not found", file=sys.stderr)
    sys.exit(1)
  print("INFO: key_dict " + json.dumps(key_dict, indent=2), file=sys.stderr)

  ret = []
  for run in json_list:
    tmp = {}
    for input_key, output_key in key_dict.items():
      tmp[output_key] = search_read(input_key, run)
    ret.append(tmp)

  return ret

def trans_to_sample_json_list(json_list, config):
  if not "sample_time_key" in config:
    print("ERROR: sample_time_key not found", file=sys.stderr)
    sys.exit(1)
  time_key = config["sample_time_key"]

  if not "sample_begin" in config:
    print("ERROR: sample_begin (yyyymmddhhmmss) not found", file=sys.stderr)
    sys.exit(1)
  sample_begin = datetime.strptime(config["sample_begin"], "%Y%m%d%H%M%S")

  if not "sample_end" in config:
    print("ERROR: sample_end (yyyymmddhhmmss) not found", file=sys.stderr)
    sys.exit(1)
  sample_end = datetime.strptime(config["sample_end"], "%Y%m%d%H%M%S")

  if not "sample_interval" in config:
    print("ERROR: sample_interval (sec) not found", file=sys.stderr)
    sys.exit(1)
  sample_interval = timedelta(seconds=int(config["sample_interval"]))

  ret = []
  json_list.sort(key=lambda x: x[time_key])

  sample_time = sample_begin
  while sample_time <= sample_end:
    index = 0
    for index, run in enumerate(json_list):
      if datetime.strptime(run[time_key], "%Y%m%d%H%M%S") < sample_time : continue
      ret.append(run)
      break
    json_list = json_list[index:-1]

    sample_time += sample_interval
  return ret

def trans_to_percentile_json_list(json_list, config, default_data_key_list):
  if len(json_list) == 0:
    return []

  if "division_number" not in config:
    print("ERROR: division_number is not found in config", file=sys.stderr)
    sys.exit()
  div = config["division_number"]

  key_list = join_run_data_key_list(default_run_key_list(), default_data_key_list, config)

  if "percentile" in key_list:
    del key_list["percentile"]

  ret = []
  for i in range(div):
    ret.append({"percentile":i})

  for key in key_list:
    tmp = []
    for run in json_list:
      tmp.append(search_read(key, run))
    tmp = list(filter(lambda x: x != "", tmp))
    tmp.sort()

    for i in range(div):
      if len(tmp) == 0:
        ret[i] = ""
      else:
        index = int((len(tmp)-1)*i/div)
        value = tmp[index]
        ret[i] = search_write(key, value, ret[i])
  return ret

def join_run_data_key_list(default_run_key_list, default_data_key_list, config):
  if "run_key_list"  in config: run_key_list  = config["run_key_list"]
  else:                         run_key_list  = default_run_key_list
  if "data_key_list" in config: data_key_list = config["data_key_list"]
  else:                         data_key_list = default_data_key_list
  key_list = run_key_list + list(map(lambda x: "data." + x, data_key_list))
  print("INFO: csv_key: " + json.dumps(key_list, indent=2), file=sys.stderr)
  return key_list
