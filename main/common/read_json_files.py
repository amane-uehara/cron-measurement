import json
import sys
from common.fetch_filelist import fetch_filelist

def fetch_json_list(config):
  load_file_list = fetch_filelist(config["load_file_list"])

  join_list = []
  for json_file in load_file_list:
    with open(json_file, 'r') as f:
      json_data = json.load(f)
      if isinstance(json_data, dict):
        join_list.append(json_data)
      if isinstance(json_data, list):
        join_list += json_data

  sorted_list = sorted(join_list, key=custom_sort)
  return sorted_list

def custom_sort(item):
  if "dt" in item:
    dt = item["dt"]
  else:
    dt = ""

  if "mac_addr" in item:
    mac_addr = item["mac_addr"]
  else:
    mac_addr = ""

  return (dt, mac_addr)

def fetch_list_list(config, default_data_key_list):
  if "run_key_list"  in config: run_key_list  = config["run_key_list"]
  else:                         run_key_list  = default_run_key_list()
  if "data_key_list" in config: data_key_list = config["data_key_list"]
  else:                         data_key_list = default_data_key_list
  key_list = run_key_list + list(map(lambda x: "data." + x, data_key_list))
  print("csv_key: " + str(key_list), file=sys.stderr)

  json_list = fetch_json_list(config)

  ret = []

  for run in json_list:
    tmp = []
    for dot_key in key_list:
      tmp.append(key_search(dot_key.split("."), run))
    ret.append(tmp)

  return ret

def key_search(layer_list, data_dict):
  key = layer_list.pop(0)

  if key not in data_dict:
    return ""
  elif len(layer_list) == 0:
    return data_dict[key]
  elif len(layer_list) >= 1:
    return key_search(layer_list, data_dict[key])

def default_run_key_list():
  return [
    "dt",
    "hostname",
    "mac_addr",
    "sensor_mac_addr",
    "sensor_location"
  ]
