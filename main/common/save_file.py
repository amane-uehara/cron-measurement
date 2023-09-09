import os
import sys
import json
import gzip

from datetime import datetime
from uuid import getnode
from common.read_config_file import apply_time_template

def save_file(text, config):
  filename = config["save_file"]
  filepath = os.path.dirname(filename)
  os.makedirs(filepath, mode=0o777, exist_ok=True)

  ext = filename.split(".")[-1]
  if ext == "gz":
    with gzip.open(filename, mode="wt") as f:
      f.write(text)
      print("gip file saved: " + filename, end="", file=sys.stderr)

  else:
    with open(filename, "w") as f:
      f.write(text)
      print("text file saved: " + filename, end="",  file=sys.stderr)

  print(" (" + str(os.path.getsize(filename)) + " byte)", file=sys.stderr)

def save_raw_data(data, config):
  run = {}
  run["dt"]  = datetime.now().strftime("%Y%m%d%H%M%S")
  run["hostname"] = config["hostname"]
  run["mac_addr"] = hex(getnode())[2:]

  if "sensor_mac_addr" in config:
    run["sensor_mac_addr"] = config["sensor_mac_addr"].lower().replace(":","")
  if "sensor_location" in config:
    run["sensor_location"] = config["sensor_location"]

  run["data"] = data
  apply_time = apply_time_template(config, run["dt"])
  save_json_file(run, apply_time)

def save_json_file(json_list, config):
  text = json.dumps(json_list, separators=(',',':'))
  save_file(text, config)

def save_csv_file(list_list, config):
  text = str(json.dumps(list_list, separators=(',',':')).replace("],[", "\n").lstrip("[[")).rstrip("\n").rstrip("]]")
  save_file(text, config)
