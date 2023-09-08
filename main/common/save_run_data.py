import json
from datetime import datetime
from uuid import getnode as get_mac
from common.read_config import apply_time_template
from common.save_file import save_file

def save_run_data(data, config):
  run = {}
  run['dt']  = datetime.now().strftime("%Y%m%d%H%M%S")
  run["hostname"] = config["hostname"]
  run['mac_addr'] = hex(get_mac())[2:]

  if "sensor_mac_addr" in config:
    run['sensor_mac_addr'] = config["sensor_mac_addr"].lower().replace(':','')
  if "sensor_location" in config:
    run['sensor_location'] = config["sensor_location"]

  run["data"] = data

  apply_time = apply_time_template(config, run["dt"])
  save_file(json.dumps(run), apply_time)

def default_run_key_list():
  return [
    "dt",
    "hostname",
    "mac_addr",
    "sensor_mac_addr",
    "sensor_location"
  ]
