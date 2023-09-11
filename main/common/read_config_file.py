import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

def read_config_file(arg_dict):
  with open(arg_dict["config_abspath"]) as f:
    try:
      config_all = json.load(f)
    except FileNotFoundError as err:
      print("ERROR: config file: `" + ret["config_abspath"] + "` not found", file=sys.stderr)
      sys.exit(1)

  title = arg_dict["title"]
  if not title in config_all:
    print("ERROR: invalid title: " + title, file=sys.stderr)
    sys.exit(1)

  config_all["constant"]["yyyymmddhhmmss"] = arg_dict["yyyymmddhhmmss"]
  config_all = replace_config_time(config_all, arg_dict["yyyymmddhhmmss"])

  constant = config_all["constant"].copy()
  target   = config_all[title].copy()

  for kc, vc in constant.items():
    if not kc in target:
      target[kc] = vc

  target = replace_self(target)
  ret = format_config(target)

  print("INFO: config: " + str(ret), file=sys.stderr)
  return ret

def replace_config_time(config, yyyymmddhhmmss):
  day_dict = {}
  t = datetime.strptime(yyyymmddhhmmss, "%Y%m%d%H%M%S")
  day_dict["yyyymmddhhmmss"] = t.strftime("%Y%m%d%H%M%S")
  day_dict["yyyymmdd"] = t.strftime("%Y%m%d")
  day_dict["hhmmss"] = t.strftime("%H%M%S")
  day_dict["yyyy"] = t.strftime("%Y")
  day_dict["hh"] = t.strftime("%H")
  day_dict["mm"] = t.strftime("%M")
  day_dict["ss"] = t.strftime("%S")

  for delay in range(366): # 1 year
    day_dict["yyyymmdd-" + str(delay) + ""] = (t - timedelta(days=delay)).strftime("%Y%m%d")
    day_dict["yyyymmdd+" + str(delay) + ""] = (t + timedelta(days=delay)).strftime("%Y%m%d")

  for delay in range(169): # 1 week
    day_dict["yyyymmddhh-" + str(delay) + ""] = (t - timedelta(hours=delay)).strftime("%Y%m%d%H")
    day_dict["yyyymmddhh+" + str(delay) + ""] = (t + timedelta(hours=delay)).strftime("%Y%m%d%H")

  for delay in range(1441): # 1 day
    day_dict["yyyymmddhhmm-" + str(delay) + ""] = (t - timedelta(minutes=delay)).strftime("%Y%m%d%H%M")
    day_dict["yyyymmddhhmm+" + str(delay) + ""] = (t + timedelta(minutes=delay)).strftime("%Y%m%d%H%M")

  for delay in range(3601): # 1 hour
    day_dict["yyyymmddhhmmss-" + str(delay) + ""] = (t - timedelta(seconds=delay)).strftime("%Y%m%d%H%M%S")
    day_dict["yyyymmddhhmmss+" + str(delay) + ""] = (t + timedelta(seconds=delay)).strftime("%Y%m%d%H%M%S")

  ret = replace_config_variable(config, day_dict)
  return ret

def replace_config_variable(config, replacer):
  ret = config.copy()

  for kc, vc in replacer.items():
    if isinstance(vc, str) or isinstance(vc, int) or isinstance(vc, float):
      ret = json.loads(json.dumps(ret).replace("${" + str(kc) + "}", str(vc)))

  return ret

def replace_self(target):
  ret = target.copy()

  for kc in target.keys():
    vc = ret[kc]
    if isinstance(vc, str) or isinstance(vc, int) or isinstance(vc, float):
      ret = json.loads(json.dumps(ret).replace("${" + str(kc) + "}", str(vc)))

  return ret

def format_config(config):
  ret = config.copy()
  for key in ["mac_addr", "sensor_mac_addr"]:
    if key in ret:
      ret[key] = ret[key].lower().replace(":","")
  return ret
