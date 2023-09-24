from typing import List, Dict, Union, Any
import sys
import json
from math import floor
from datetime import datetime, timedelta

def search_read(
  key_str:   str,
  data_dict: Dict[str, Any]
) -> Dict[str, Any]:

  key_list = key_str.split(".")
  key = key_list.pop(0)

  if not isinstance(data_dict, dict):
    return {"": ""}

  if key not in data_dict:
    return {"": ""}

  if len(key_list) == 0:
    value = data_dict[key]
    return {"": data_dict[key]}

  if len(key_list) >= 1:
    return search_read(".".join(key_list), data_dict[key])

  return {"": ""}

def search_write(
  key_str:   str,
  value:     Any,
  data_dict: Dict[str, Any]
) -> Dict[str, Any]:

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

def default_run_key_list() -> List[str]:
  return [
    "dt",
    "yyyymmdd",
    "hostname",
    "mac_addr"
  ]

def trans_to_list_list(
  json_list: List[Dict[str, Any]],
  config: Dict[str, Any],
  default_data_key_list: List[str]
) -> List[List[Union[None, str, int, float, bool]]]:

  key_list = join_run_data_key_list(default_run_key_list(), default_data_key_list, config)

  ret = []
  for run in json_list:
    tmp: List[Union[None, str, int, float, bool]] = []
    for dot_key in key_list:
      value_dict = search_read(dot_key, run)
      value = value_dict[""]
      if isinstance(value, str) or isinstance(value, int) or isinstance(value, float) or isinstance(value, bool):
        tmp.append(value)
      else:
        tmp.append("")
    ret.append(tmp)

  return ret

def trans_to_selected_json_list(
  json_list: List[Dict[str, Any]],
  config: Dict[str, Any]
) -> List[Dict[str, Any]]:

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
       value_dict = search_read(input_key, run)
       tmp["output_key"] = value_dict[""]
    ret.append(tmp)

  return ret

def trans_to_sample_json_list(
  json_list: List[Dict[str, Any]],
  config: Dict[str, Any]
) -> List[Dict[str, Any]]:

  if not "sample_time_key" in config:
    print("ERROR: sample_time_key not found", file=sys.stderr)
    sys.exit(1)
  time_key = config["sample_time_key"]

  if not "sample_begin" in config:
    print("ERROR: sample_begin (yyyymmddhhmmss) not found", file=sys.stderr)
    sys.exit(1)
  sample_time = datetime.strptime(config["sample_begin"], "%Y%m%d%H%M%S")

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

  for run in json_list:
    run_time = datetime.strptime(run[time_key], "%Y%m%d%H%M%S")
    if sample_time <= run_time and run_time < sample_time + sample_interval:
      ret.append(run.copy())
      sample_time += sample_interval
    if sample_end <= sample_time: break

  return ret

def trans_to_percentile_json_list(
  json_list: List[Dict[str, Any]],
  config: Dict[str, Any],
  default_data_key_list: List[str]
) -> List[Dict[str, Any]]:

  if len(json_list) == 0:
    return []

  if "division_number" not in config:
    print("ERROR: division_number is not found in config", file=sys.stderr)
    sys.exit()
  div = config["division_number"]

  key_list = join_run_data_key_list(default_run_key_list(), default_data_key_list, config)

  if "percentile" in key_list:
    key_list.remove("percentile")

  ret = []
  for i in range(div):
    ret.append({"percentile":i})

  for key in key_list:
    tmp = []
    for run in json_list:
      value_dict = search_read(key, run)
      tmp.append(value_dict[""])
    tmp = list(filter(lambda x: x != "", tmp))
    tmp.sort()

    for i in range(div):
      if len(tmp) == 0:
        ret[i] = {}
      else:
        index = int((len(tmp)-1)*i/div)
        value = tmp[index]
        ret[i] = search_write(key, value, ret[i])
  return ret

def join_run_data_key_list(
  default_run_key_list:  List[str],
  default_data_key_list: List[str],
  config: Dict[str, Any]
) -> List[str]:

  if "run_key_list"  in config: run_key_list  = config["run_key_list"]
  else:                         run_key_list  = default_run_key_list
  if "data_key_list" in config: data_key_list = config["data_key_list"]
  else:                         data_key_list = default_data_key_list
  key_list = run_key_list + list(map(lambda x: "data." + x, data_key_list))
  print("INFO: csv_key: " + json.dumps(key_list, indent=2), file=sys.stderr)
  return key_list
