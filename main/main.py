import sys
import json
from common import *

def main(argv):
  config  = read_config_file(argv)
  sensor = import_sensor(config["sensor"])
  program = config["program"]

  if program == "fetch_raw_json":
    data = sensor["fetch_json"](config)
    save_raw_data(data, config)

  if program == "to_csv":
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    list_list = fetch_list_list(apply_time, sensor["key_list"])
    save_csv_file(list_list, apply_time)

  if program == "to_json_list":
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    json_list = fetch_json_list(apply_time)
    save_json_file(json_list, apply_time)

if __name__ == "__main__":
  main(sys.argv)
