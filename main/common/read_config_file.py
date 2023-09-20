import sys
import json
import re
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

  target    = config_all[title].copy()
  constant  = config_all["constant"].copy()
  time_dict = create_time_dict(arg_dict["yyyymmddhhmmss"])

  for kc, vc in constant.items():
    if not kc in target:
      target[kc] = vc

  for kc, vc in time_dict.items():
    target[kc] = vc

  target["repository_path"] = arg_dict["repository_path"]

  target = replace_self(target)
  target = replace_config_shift_time(target, arg_dict["yyyymmddhhmmss"])
  ret = format_config(target)

  print("INFO: config: " + json.dumps(ret, indent=2), file=sys.stderr)
  return ret

def replace_config_shift_time(config, yyyymmddhhmmss):
  replacer_list = [
    {
      "match": "\${yyyymmddhhmmss[-+][0-9][0-9]*}",
      "strf" : "%Y%m%d%H%M%S",
      "delta": lambda x: timedelta(seconds=x)
    },
    {
      "match": "\${yyyymmddhhmm[-+][0-9][0-9]*}",
      "strf" : "%Y%m%d%H%M",
      "delta": lambda x: timedelta(minutes=x)
    },
    {
      "match": "\${yyyymmddhh[-+][0-9][0-9]*}",
      "strf" : "%Y%m%d%H",
      "delta": lambda x: timedelta(hours=x)
    },
    {
      "match": "\${yyyymmdd[-+][0-9][0-9]*}",
      "strf" : "%Y%m%d",
      "delta": lambda x: timedelta(days=x)
    },
    {
      "match": "\${yyyymm[-+][0-9][0-9]*}",
      "strf" : "%Y%m",
      "delta": lambda x: timedelta(months=x)
    },
    {
      "match": "\${yyyy[-+][0-9][0-9]*}",
      "strf" : "%Y",
      "delta": lambda x: timedelta(years=x)
    }
  ]

  original_time = datetime.strptime(yyyymmddhhmmss, "%Y%m%d%H%M%S")
  config_str = json.dumps(config)

  for r in replacer_list:
    item_list = re.findall(r["match"], config_str)
    for item in item_list:
      shift = int(re.findall("[-+][0-9][0-9]*", item)[0])
      value = (original_time + r["delta"](shift)).strftime(r["strf"])
      config_str = config_str.replace(item, value)

  return json.loads(config_str)

def create_time_dict(yyyymmddhhmmss):
  ret = {}

  t = datetime.strptime(yyyymmddhhmmss, "%Y%m%d%H%M%S")
  ret["yyyymmddhhmmss"] = t.strftime("%Y%m%d%H%M%S")
  ret["yyyymmddhhmm"] = t.strftime("%Y%m%d%H%M")
  ret["yyyymmddhh"] = t.strftime("%Y%m%d%H")
  ret["yyyymmdd"] = t.strftime("%Y%m%d")
  ret["yyyymm"] = t.strftime("%Y%m")
  ret["yyyy"] = t.strftime("%Y")

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
