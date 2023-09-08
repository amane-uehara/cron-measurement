import json
from json_to_json_list import fetch_json_list
from common.save_run_data import default_run_key_list

def fetch_list_list(config, default_data_key_list):
  if "run_key_list" in config:
    run_key_list = config["run_key_list"]
  else:
    run_key_list = default_run_key_list()

  if "data_key_list" in config:
    data_key_list = config["data_key_list"]
  else:
    data_key_list = default_data_key_list()

  json_list = fetch_json_list(config)

  ret = []

  for run in json_list:
    tmp = []

    for key in run_key_list:
      if key not in run:
        tmp.append("")
      else:
        tmp.append(run[key])

    for key in data_key_list:
      if key not in run["data"]:
        tmp.append("")
      else:
        tmp.append(run["data"][key])

    ret.append(tmp)

  return ret
