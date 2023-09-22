from typing import List, Dict, Union, Any, Callable
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from uuid import getnode

def read_config_file(arg_dict: Dict[str, Union[int,str]]) -> Dict[str, Any]:
  with open(arg_dict["config_abspath"]) as f:
    try:
      config_all = json.load(f)
    except FileNotFoundError as err:
      print("ERROR: config file: `" + str(arg_dict["config_abspath"]) + "` not found", file=sys.stderr)
      sys.exit(1)

  title = str(arg_dict["title"])
  if not title in config_all:
    print("ERROR: invalid title: " + title, file=sys.stderr)
    sys.exit(1)

  target    = config_all[title].copy()
  constant  = config_all["constant"].copy()
  time_dict = create_time_dict(str(arg_dict["yyyymmddhhmmss"]))

  for kc, vc in constant.items():
    if not kc in target:
      target[kc] = vc

  for kc, vc in time_dict.items():
    target[kc] = vc

  target["repository_path"] = str(arg_dict["repository_path"])
  target["dryrun"] = str(arg_dict["dryrun"])

  target["fork_main_py"] = str(arg_dict["exec_main_py"])
  target["fork_main_py"] += " --config " + str(arg_dict["config_abspath"])

  if arg_dict["dryrun"] :
    target["fork_main_py"] += " --dryrun"

  target["mac_addr"] = hex(getnode())[2:]

  target = replace_self(target)
  target = replace_config_shift_time(target, str(arg_dict["yyyymmddhhmmss"]))
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
