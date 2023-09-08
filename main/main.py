import sys
import json
import gzip
from common.read_config import read_config, apply_time_template
from common.save_run_data import save_run_data
from common.fetch_filelist import fetch_filelist

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
    mac_addr       = config["sensor_mac_addr"].lower().replace(':','')
    bt_retry_count = config["bt_retry_count"]
    bt_dev_id      = config["bt_dev_id"]
    data = omron_env_sensor.fetch_json(mac_addr, bt_retry_count, bt_dev_id)
    save_run_data(data, config)

  if program == "fetch_inkbird_env_sensor":
    import inkbird_env_sensor
    mac_addr       = config["sensor_mac_addr"].lower().replace(':','')
    bt_retry_count = config["bt_retry_count"]
    data = inkbird_env_sensor.fetch_json(mac_addr, bt_retry_count)
    save_run_data(data, config)

  if program == "json_to_list":
    yyyymmddhhmmss = argv[2]
    config = apply_time_template(config, yyyymmddhhmmss)
    print(config["load_json_files"])
    load_json_files = fetch_filelist(config["load_json_files"])
    print(load_json_files)
    save_file = config["save_file"]
    join_list = []
    for json_file in load_json_files:
      with open(json_file, 'r') as f:
        join_list.append(json.load(f))
    with gzip.open(save_file, mode='wt') as f:
      f.write(json.dumps(join_list))

if __name__ == "__main__":
  main(sys.argv)
