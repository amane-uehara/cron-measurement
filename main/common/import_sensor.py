import os
import sys
from importlib import import_module
from glob import glob

def fetch_sensor_name_list():
  main_path   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  sensor_path = os.path.join(main_path, "sensor", "*.py")
  sensor_file_list = glob(sensor_path)
  sensor_name_list = list(map(lambda x: str(os.path.basename(x))[:-3], sensor_file_list))
  return sensor_name_list

def import_sensor(sensor_name):
  ret = {}
  sensor_name_list = fetch_sensor_name_list()
  if not sensor_name in sensor_name_list:
    print("ERROR: sensor '" + sensor_name + "' is not in /main/sensor/* " + str(sensor_name_list), file=sys.stderr)
    sys.exit(1)
  else:
    print("INFO: import: sensor." + sensor_name, file=sys.stderr)
    module = import_module("sensor." + sensor_name)
    ret["fetch_json"] = module.fetch_json
    ret["key_list"]   = module.key_list()
  return ret
