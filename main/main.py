import sys
import json
from common.read_config import read_config, apply_time_template
from common.save_run_data import save_run_data
from common.fetch_filelist import fetch_filelist
from common.save_file import save_file
from common.json_to_list_list import fetch_list_list

def main(argv):
  title = argv[1]
  config = read_config(argv)
  program = config["program"]

  if program == "fetch_system_resource":
    import system_resource
    data = system_resource.fetch_json()
    save_run_data(data, config)

  if program == "fetch_omron_env_sensor":
    import omron_env_sensor
    data = omron_env_sensor.fetch_json(config)
    save_run_data(data, config)

  if program == "fetch_inkbird_env_sensor":
    import inkbird_env_sensor
    data = inkbird_env_sensor.fetch_json(config)
    save_run_data(data, config)

  if program == "csv_system_resource":
    import system_resource
    default_data_key_list = system_resource.key_list()
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    value_list_list = fetch_list_list(apply_time, default_data_key_list)
    csv_text = "\n".join([",".join(map(str, x)) for x in value_list_list])
    save_file(csv_text, apply_time)

  if program == "csv_omron_env_sensor":
    import omron_env_sensor
    default_data_key_list = omron_env_sensor.key_list()
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    value_list_list = fetch_list_list(apply_time, default_data_key_list)
    csv_text = "\n".join([",".join(map(str, x)) for x in value_list_list])
    save_file(csv_text, apply_time)

  if program == "csv_inkbird_env_sensor":
    import inkbird_env_sensor
    default_data_key_list = inkbird_env_sensor.key_list()
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    value_list_list = fetch_list_list(apply_time, default_data_key_list)
    csv_text = "\n".join([",".join(map(str, x)) for x in value_list_list])
    save_file(csv_text, apply_time)

  if program == "json_to_json_list":
    import json_to_json_list
    yyyymmddhhmmss = argv[2]
    apply_time = apply_time_template(config, yyyymmddhhmmss)
    data_list = json_to_json_list.fetch_json_list(apply_time)
    save_file(json.dumps(data_list), apply_time)

if __name__ == "__main__":
  main(sys.argv)
