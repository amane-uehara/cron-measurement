import sys
import json
from common import *

def main():
  arg_dict = read_arg()
  config  = read_config_file(arg_dict)
  sensor  = import_sensor(config["sensor"])
  program = config["program"]

  if program == "fetch_raw_json":
    data = sensor["fetch_json"](config)
    save_raw_data(data, config)

  if program == "to_json_list":
    json_list = fetch_json_list(config)
    save_json_file(json_list, config)

  if program == "to_csv":
    json_list = fetch_json_list(config)
    list_list = trans_to_list_list(json_list, config, sensor["key_list"])
    save_csv_file(list_list, config)

  if program == "to_selected_json_list":
    json_list = fetch_json_list(config)
    selected_json_list = trans_to_selected_json_list(json_list, config)
    save_json_file(selected_json_list, config)

  if program == "to_sample_json_list":
    json_list = fetch_json_list(config)
    sample_json_list = trans_to_sample_json_list(json_list, config)
    save_json_file(sample_json_list, config)

  if program == "to_sample_csv":
    json_list = fetch_json_list(config)
    sample_json_list = trans_to_sample_json_list(json_list, config)
    list_list = trans_to_list_list(sample_json_list, config, sensor["key_list"])
    save_csv_file(list_list, config)

  if program == "to_percentile_json_list":
    json_list = fetch_json_list(config)
    selected_json_list = trans_to_percentile_json_list(json_list, config, sensor["key_list"])
    save_json_file(selected_json_list, config)

if __name__ == "__main__":
  main()
