from typing import List, Dict, Union, Any, Callable
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

def read_config_file(arg: Dict[str, str]) -> Dict[str, Any]:
  with open(arg["config_abspath"]) as f:
    try:
      raw_config = json.load(f)
    except FileNotFoundError as err:
      print("ERROR: config file: `" + arg["config_abspath"] + "` not found", file=sys.stderr)
      sys.exit(1)
  return raw_config

def join_arg_config(
  arg: Dict[str, str],
  raw_config: Dict[str, Any]
) -> Dict[str, Any]:

  title = arg["title"]
  if not title in raw_config:
    print("ERROR: invalid title: " + title, file=sys.stderr)
    sys.exit(1)

  target    = raw_config[title].copy()
  constant  = raw_config["constant"].copy()
  time_dict = create_time_dict(arg["yyyymmddhhmmss"])

  for kc, vc in constant.items():
    if not kc in target:
      target[kc] = vc

  for kc, vc in time_dict.items():
    target[kc] = vc

  target["repository_path"] = arg["repository_path"]
  target["dryrun"] = arg["dryrun"]

  target["fork_main_py"] = arg["exec_main_py"]
  target["fork_main_py"] += " --config " + arg["config_abspath"]

  if arg["dryrun"] == "True":
    target["fork_main_py"] += " --dryrun"

  target["mac_addr"] = arg["mac_addr"]

  target = replace_self(target)
  target = replace_config_shift_time(target, arg["yyyymmddhhmmss"])
  ret = format_config(target)

  print("INFO: config: " + json.dumps(ret, indent=2), file=sys.stderr)
  return ret

def replace_config_shift_time(config: Dict[str, Any], yyyymmddhhmmss: str) -> Dict[str, Any]:
  replacer_list: List[Dict[str,str]] = [
    {
      "match": "\${yyyymmddhhmmss[-+][0-9][0-9]*}",
      "strf" : "%Y%m%d%H%M%S",
    },
    {
      "match": "\${yyyymmddhhmm[-+][0-9][0-9]*}",
      "strf" : "%Y%m%d%H%M",
    },
    {
      "match": "\${yyyymmddhh[-+][0-9][0-9]*}",
      "strf" : "%Y%m%d%H",
    },
    {
      "match": "\${yyyymmdd[-+][0-9][0-9]*}",
      "strf" : "%Y%m%d",
    }
  ]

  timedelta_func_list: List[Callable[[int],timedelta]] = [
    (lambda x: timedelta(seconds=x)),
    (lambda x: timedelta(minutes=x)),
    (lambda x: timedelta(hours=x)),
    (lambda x: timedelta(days=x))
  ]

  original_time = datetime.strptime(yyyymmddhhmmss, "%Y%m%d%H%M%S")
  config_str = json.dumps(config)

  for i, r in enumerate(replacer_list):
    timedelta_func = timedelta_func_list[i]
    item_list = re.findall(str(r["match"]), str(config_str))
    for item in item_list:
      shift = int(re.findall("[-+][0-9][0-9]*", item)[0])
      value = (original_time + timedelta_func(shift)).strftime(r["strf"])
      config_str = config_str.replace(item, value)

  return json.loads(config_str)

def create_time_dict(yyyymmddhhmmss: str) -> Dict[str,str]:
  ret = {}

  t = datetime.strptime(yyyymmddhhmmss, "%Y%m%d%H%M%S")
  ret["yyyymmddhhmmss"] = t.strftime("%Y%m%d%H%M%S")
  ret["yyyymmddhhmm"] = t.strftime("%Y%m%d%H%M")
  ret["yyyymmddhh"] = t.strftime("%Y%m%d%H")
  ret["yyyymmdd"] = t.strftime("%Y%m%d")
  ret["yyyymm"] = t.strftime("%Y%m")
  ret["yyyy"] = t.strftime("%Y")

  return ret

def replace_config_variable(
  config:   Dict[str, Any],
  replacer: Dict[str, Union[str, int, float]]
) -> Dict[str, Any]:

  ret = config.copy()

  for kc, vc in replacer.items():
    if isinstance(vc, str) or isinstance(vc, int) or isinstance(vc, float):
      ret = json.loads(json.dumps(ret).replace("${" + str(kc) + "}", str(vc)))

  return ret

def replace_self(target: Dict[str, Any]) -> Dict[str, Any]:
  ret = target.copy()

  for kc in target.keys():
    vc = ret[kc]
    if isinstance(vc, str) or isinstance(vc, int) or isinstance(vc, float):
      ret = json.loads(json.dumps(ret).replace("${" + str(kc) + "}", str(vc)))

  return ret

def format_config(config: Dict[str, Any]) -> Dict[str, Any]:
  ret = config.copy()
  for key in ["mac_addr", "sensor_mac_addr"]:
    if key in ret:
      ret[key] = ret[key].lower().replace(":","")
  return ret
