import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def read_config(argv):
  config_filename = str(Path(__file__).resolve().parent.parent.parent.joinpath('config.json'))
  for v in argv:
    if "--config=" in v:
      config_filename = v.split("=",1)[1]

  with open(config_filename) as f:
    try:
      config_all = json.load(f)
    except FileNotFoundError as err:
      print("invalid config file: " + config_filename, file=sys.stderr)
      sys.exit(1)

  title = argv[1]
  if not title in config_all:
    print("invalid title: " + title, file=sys.stderr)
    sys.exit(1)

  config   = config_all[title].copy()
  constant = config_all["constant"].copy()

  for kc, vc in constant.items():
    config = json.loads(json.dumps(config).replace("{" + str(kc) + "}", vc))

  for kc, vc in config.items():
    constant[kc] = vc

  return constant

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
    config = json.loads(json.dumps(config).replace("{" + str(kc) + "}", vc))

  return config
