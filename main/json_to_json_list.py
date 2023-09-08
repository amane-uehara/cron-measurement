import json
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