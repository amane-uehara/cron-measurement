import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

def read_config_file(argv):
  config_filename = str(Path(__file__).resolve().parent.parent.parent.joinpath("config.json"))
  for v in argv:
    if "--config=" in v:
      config_filename = v.split("=",1)[1]

  with open(config_filename) as f:
    try:
      config_all = json.load(f)
    except FileNotFoundError as err:
      print("ERROR: invalid config file: " + config_filename, file=sys.stderr)
      sys.exit(1)

  title = argv[1]
  if not title in config_all:
    print("ERROR: invalid title: " + title, file=sys.stderr)
    sys.exit(1)

  target = config_all[title].copy()

  for kc, vc in config_all[title].items():
    if isinstance(vc, str) or isinstance(vc, int) or isinstance(vc, float):
      target = json.loads(json.dumps(target).replace("${" + str(kc) + "}", vc))

  for kc, vc in config_all["constant"].items():
    if isinstance(vc, str) or isinstance(vc, int) or isinstance(vc, float):
      target = json.loads(json.dumps(target).replace("${" + str(kc) + "}", vc))

  ret = config_all["constant"].copy()
  for kc, vc in target.items():
    ret[kc] = vc

  for key in ["mac_addr", "sensor_mac_addr"]:
    if key in ret:
      ret[key] = ret[key].lower().replace(":","")

  return ret

def apply_time_template(config, yyyymmddhhmmss):
  day_dict = {}
  t = datetime.strptime(yyyymmddhhmmss, "%Y%m%d%H%M%S")
  day_dict["yyyymmddhhmmss"] = t.strftime("%Y%m%d%H%M%S")
  day_dict["yyyymmdd"] = t.strftime("%Y%m%d")
  day_dict["hhmmss"] = t.strftime("%H%M%S")
  day_dict["yyyy"] = t.strftime("%Y")
  day_dict["hh"] = t.strftime("%H")
  day_dict["mm"] = t.strftime("%M")
  day_dict["ss"] = t.strftime("%S")

  for delay in range(366):
    day_dict["yyyymmdd-" + str(delay) + ""] = (t - timedelta(days=delay)).strftime("%Y%m%d")
    day_dict["yyyymmdd+" + str(delay) + ""] = (t + timedelta(days=delay)).strftime("%Y%m%d")

  for kc, vc in day_dict.items():
    config = json.loads(json.dumps(config).replace("${" + str(kc) + "}", vc))

  return config
