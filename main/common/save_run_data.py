import os
import json
from datetime import datetime
from uuid import getnode as get_mac
from common.read_config import apply_time_template

def save_run_data(data, config):
  run = {}
  run['dt']  = datetime.now().strftime("%Y%m%d%H%M%S")
  run["hostname"] = config["hostname"]
  run['mac_addr'] = hex(get_mac())[2:]
  if "sensor_mac_addr" in config:
    run['sensor_mac_addr'] = config["sensor_mac_addr"].lower().replace(':','')
  run["data"] = data

  apply_time = apply_time_template(config, run["dt"])
  filename = apply_time["save_file"]
  filepath = os.path.dirname(filename)
  os.makedirs(filepath, mode=0o777, exist_ok=True)

  with open(filename, 'w') as f:
    f.write(json.dumps(run))
