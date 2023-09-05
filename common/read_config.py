import json
import sys
from datetime import datetime, timedelta

def read_config(config_filename, yyyymmddhhmmss):
  day_dict = {}

  now = datetime.strptime(yyyymmddhhmmss, "%Y%m%d%H%M%S")
  day_dict["yyyymmddhhmmss"] = now.strftime("%Y%m%d%H%M%S")
  day_dict["yyyymmdd"] = now.strftime("%Y%m%d")
  day_dict["hhmmss"] = now.strftime("%H%M%S")
  day_dict["yyyy"] = now.strftime("%Y")
  day_dict["hh"] = now.strftime("%H")
  day_dict["mm"] = now.strftime("%M")
  day_dict["ss"] = now.strftime("%S")

  for delay in range(366):
    day_dict["yyyymmdd-" + str(delay) + ""] = (now - timedelta(days=delay)).strftime("%Y%m%d")
    day_dict["yyyymmdd+" + str(delay) + ""] = (now + timedelta(days=delay)).strftime("%Y%m%d")

  with open(config_filename) as f:
    config = json.load(f)

  constant = config["constant"].copy()

  for title, target in config.items():
    if title == "constant" : continue
    for kt, vt in target.items():
      target[kt] = vt.replace("{title}", title)

  for kc, vc in {**constant, **day_dict}.items():
    for title, target in config.items():
      if title == "constant" : continue
      for kt, vt in target.items():
        target[kt] = vt.replace("{" + str(kc) + "}", vc)

  return config


if __name__ == "__main__":
  data = read_config(sys.argv[1], sys.argv[2])
  print(json.dumps(data))
