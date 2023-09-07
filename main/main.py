import sys
import json
import gzip
import common.json_to_list_gz
from common.read_config import read_raw_config, apply_template
from common.save_run_data import save_run_data
from common.fetch_filelist import fetch_filelist

def main(argv):
  title = argv[1]
  raw_config = read_raw_config(argv)
  program = raw_config[title]["program"]

  if program == "fetch_system_resource":
    import system_resource
    data = system_resource.fetch_json()
    save_run_data(data, title, raw_config)

  if program == "fetch_omron_env_sensor":
    import omron_env_sensor
    mac_addr = raw_config[title]["sensor_mac_addr"].lower().replace(':','')
    bt_retry_count = raw_config[title]["bt_retry_count"]
    bt_dev_id      = raw_config[title]["bt_dev_id"]
    data = omron_env_sensor.fetch_json(mac_addr, bt_retry_count, bt_dev_id)
    data["sensor_mac_addr"] = mac_addr
    save_run_data(data, title, raw_config)

  if program == "fetch_inkbird_env_sensor":
    import inkbird_env_sensor
    mac_addr = raw_config[title]["sensor_mac_addr"].lower().replace(':','')
    bt_retry_count = raw_config[title]["bt_retry_count"]
    data = inkbird_env_sensor.fetch_json(mac_addr, bt_retry_count)
    data["sensor_mac_addr"] = mac_addr
    save_run_data(data, title, raw_config)

  if program == "json_to_list":
    yyyymmddhhmmss = argv[2]
    config = apply_template(raw_config, yyyymmddhhmmss)
    print(config[title]["load_json_files"])
    load_json_files = fetch_filelist(config[title]["load_json_files"])
    print(load_json_files)
    save_file = config[title]["save_json_gz_file"]
    join_list = []
    for json_file in load_json_files:
      with open(json_file, 'r') as f:
        join_list.append(json.load(f))
    with gzip.open(save_file, mode='wt') as f:
      f.write(json.dumps(join_list))

if __name__ == "__main__":
  main(sys.argv)
