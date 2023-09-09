import sys
import json
from common.read_config_file import read_config_file, apply_time_template
from common.save_file import save_file, save_run_data
from common.read_json_files import fetch_list_list, fetch_json_list

def main(argv):
  title = argv[1]
  config = read_config_file(argv)
  program = config["program"]

  if "system_resource" in program:
    import sensor.system_resource
    fetch_json = sensor.system_resource.fetch_json
    default_data_key_list = sensor.system_resource.key_list()

  if "omron_env_sensor" in program:
    import sensor.omron_env_sensor
    fetch_json = sensor.omron_env_sensor.fetch_json
    default_data_key_list = sensor.omron_env_sensor.key_list()

  if "inkbird_env_sensor" in program:
    import sensor.inkbird_env_sensor
    fetch_json = sensor.inkbird_env_sensor.fetch_json
    default_data_key_list = sensor.inkbird_env_sensor.key_list()

  if "fetch_" in program:
    data = fetch_json(config)
    save_run_data(data, config)

  if "csv_" in program:
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    value_list_list = fetch_list_list(apply_time, default_data_key_list)
    csv_text = "\n".join([",".join(map(str, x)) for x in value_list_list])
    save_file(csv_text, apply_time)

  if program == "json_list_":
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    data_list = fetch_json_list.fetch_json_list(apply_time)
    save_file(json.dumps(data_list), apply_time)

if __name__ == "__main__":
  main(sys.argv)
