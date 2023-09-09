import sys
import json
from importlib import import_module
from common.read_config_file import read_config_file, apply_time_template
from common.save_file import save_file, save_run_data
from common.read_json_files import fetch_list_list, fetch_json_list

def main(argv):
  config  = read_config_file(argv)
  sensor  = config["sensor"]
  program = config["program"]

  if not sensor:
    sensor_fetch_json = None
    sensor_key_list = None
  else:
    module = import_module("sensor." + sensor)
    sensor_fetch_json = module.fetch_json
    sensor_key_list = module.key_list

  if program == "fetch_raw_json":
    data = sensor_fetch_json(config)
    save_run_data(data, config)

  if program == "to_csv":
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    value_list_list = fetch_list_list(apply_time, sensor_key_list())
    csv_text = "\n".join([",".join(map(str, x)) for x in value_list_list])
    save_file(csv_text, apply_time)

  if program == "to_json_list":
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    data_list = fetch_json_list.fetch_json_list(apply_time)
    save_file(json.dumps(data_list), apply_time)

if __name__ == "__main__":
  main(sys.argv)
