import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def read_raw_config(argv):
  config_filename = str(Path(__file__).resolve().parent.parent.parent.joinpath('config.json'))
  for v in argv:
    if "--config=" in v:
      config_filename = v.split("=",1)[1]

  with open(config_filename) as f:
    config = json.load(f)
  return config

def apply_template(raw_config, yyyymmddhhmmss):
  config = raw_config.copy()

  t = datetime.strptime(yyyymmddhhmmss, "%Y%m%d%H%M%S")
  config["constant"]["yyyymmddhhmmss"] = t.strftime("%Y%m%d%H%M%S")
  config["constant"]["yyyymmdd"] = t.strftime("%Y%m%d")
  config["constant"]["hhmmss"] = t.strftime("%H%M%S")
  config["constant"]["yyyy"] = t.strftime("%Y")
  config["constant"]["hh"] = t.strftime("%H")
  config["constant"]["mm"] = t.strftime("%M")
  config["constant"]["ss"] = t.strftime("%S")

  for delay in range(366):
    config["constant"]["yyyymmdd-" + str(delay) + ""] = (t - timedelta(days=delay)).strftime("%Y%m%d")
    config["constant"]["yyyymmdd+" + str(delay) + ""] = (t + timedelta(days=delay)).strftime("%Y%m%d")

  constant = config["constant"].copy()

  for kc, vc in constant.items():
    for title, target in config.items():
      if title == "constant" : continue
      for kt, vt in target.items():
        if not type(vt) is str: continue
        target[kt] = vt.replace("{" + str(kc) + "}", vc)

  return config

def read_config(argv, yyyymmddhhmmss):
  raw_config = read_raw_config(argv)
  config = apply_template(raw_config, yyyymmddhhmmss)
  return config

if __name__ == "__main__":
  yyyymmddhhmmss = sys.argv[1]
  config = read_config(argv, yyyymmddhhmmss)
  print(json.dumps(config))
