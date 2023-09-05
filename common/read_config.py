import json
import sys
from datetime import date, timedelta

def read_config(config_filename):
  day_dict = {}
  today = date.today()
  day_dict["yyyymmdd"] = today.strftime("%Y%m%d")
  for delay in range(366):
    day_dict["yyyymmdd-" + str(delay) + ""] = (today - timedelta(days=delay)).strftime("%Y%m%d")
    day_dict["yyyymmdd+" + str(delay) + ""] = (today + timedelta(days=delay)).strftime("%Y%m%d")

  with open(config_filename) as f:
    config = json.load(f)

  constant = config["constant"].copy()
  del config["constant"]

  for title, target in config.items():
    for kt, vt in target.items():
      target[kt] = vt.replace("{title}", title)

  for kc, vc in {**constant, **day_dict}.items():
    for title, target in config.items():
      for kt, vt in target.items():
        target[kt] = vt.replace("{" + str(kc) + "}", vc)

  return config


if __name__ == "__main__":
  data = read_config(sys.argv[1])
  print(json.dumps(data))
