import sys
import json
from common.read_config_file import read_config_file, apply_time_template
from common.save_file import save_file, save_run_data
from common.read_json_files import fetch_list_list, fetch_json_list
from common.import_sensor import import_sensor

def main(argv):
  config  = read_config_file(argv)

  sensor = import_sensor(config["sensor"])
  fetch_json = sensor["fetch_json"]
  key_list   = sensor["key_list"]

  program = config["program"]

  if program == "fetch_raw_json":
    data = fetch_json(config)
    save_run_data(data, config)

  if program == "to_csv":
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    value_list_list = fetch_list_list(apply_time, key_list())
    csv_text = "\n".join([",".join(map(str, x)) for x in value_list_list])
    save_file(csv_text, apply_time)

  if program == "to_json_list":
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    data_list = fetch_json_list.fetch_json_list(apply_time)
    save_file(json.dumps(data_list), apply_time)

if __name__ == "__main__":
  main(sys.argv)
