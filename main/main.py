import sys
import json
from common.read_config_file import read_config_file, apply_time_template
from common.fetch_filelist import fetch_filelist
from common.save_file import save_file, save_run_data
from common.read_json_files import fetch_list_list, json_to_json_list

def main(argv):
  title = argv[1]
  config = read_config_file(argv)
  program = config["program"]

  if "system_resource" in program:
    import system_resource
    fetch_json = system_resource.fetch_json
    default_data_key_list = system_resource.key_list()

  if "omron_env_sensor" in program:
    import omron_env_sensor
    data = omron_env_sensor.fetch_json()
    save_run_data(data, config)

  if "inkbird_env_sensor" in program:
    import inkbird_env_sensor
    data = inkbird_env_sensor.fetch_json()
    save_run_data(data, config)

  if "fetch_" in program:
    data = fetch_json()
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
    data_list = json_to_json_list.fetch_json_list(apply_time)
    save_file(json.dumps(data_list), apply_time)

if __name__ == "__main__":
  main(sys.argv)
