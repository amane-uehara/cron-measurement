from typing import List, Dict, Union, Any
import sys
import json
from common import *

def main():
  arg_dict: Dict[str, Any] = read_arg()
  config:   Dict[str, Any] = read_config_file(arg_dict)
  sensor:   Dict[str, Any] = import_sensor(config["sensor"])
  program:  str            = config["program"]

  data:               Dict[str, Any]
  json_list:          List[Dict[str, Any]]
  list_list:          List[List[Union[None, str, int, float, bool]]]
  selected_json_list: List[Dict[str, Any]]
  sample_json_list:   List[Dict[str, Any]]

  if program == "fetch_raw_json":
    data = sensor["fetch_json"](config)
    save_raw_data(data, config)

  else:
    json_list = fetch_json_list(config)

    if program == "to_json_list":
      save_json_file(json_list, config)

    elif program == "to_csv":
      list_list = trans_to_list_list(json_list, config, sensor["key_list"])
      save_csv_file(list_list, config)

    elif program == "to_selected_json_list":
      selected_json_list = trans_to_selected_json_list(json_list, config)
      save_json_file(selected_json_list, config)

    elif program == "to_sample_json_list":
      sample_json_list = trans_to_sample_json_list(json_list, config)
      save_json_file(sample_json_list, config)

    elif program == "to_sample_csv":
      sample_json_list = trans_to_sample_json_list(json_list, config)
      list_list = trans_to_list_list(sample_json_list, config, sensor["key_list"])
      save_csv_file(list_list, config)

    elif program == "to_percentile_json_list":
      selected_json_list = trans_to_percentile_json_list(json_list, config, sensor["key_list"])
      save_json_file(selected_json_list, config)

if __name__ == "__main__":
  main()
