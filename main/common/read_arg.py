from typing import List, Dict, Union, Any
import os
import sys
import argparse
import json
from datetime import datetime
from uuid import getnode

def read_domain() -> Dict[str, str]:
  ret = {}
  ret["current_path"] = os.getcwd()
  ret["repository_path"] = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  ret["default_config_file"] = os.path.join(ret["repository_path"], "config.json")
  ret["sys_executable"] = sys.executable
  ret["now_yyyymmddhhmmss"] = datetime.now().strftime("%Y%m%d%H%M%S")
  ret["mac_addr"] = hex(getnode())[2:]
  return ret

def read_arg(domain: Dict[str, str]) -> Dict[str, str]:
  parser = argparse.ArgumentParser()
  parser.add_argument("title", type=str)
  parser.add_argument("--yyyymmddhhmmss", type=str, default=domain["now_yyyymmddhhmmss"])
  parser.add_argument("--config", type=str, default=domain["default_config_file"])
  parser.add_argument("--dryrun", action="store_true")
  args = parser.parse_args()

  ret = vars(args)
  ret.update(domain)

  ret["exec_main_py"] = domain["sys_executable"] + " " + sys.argv[0]
  ret["config_abspath"] = os.path.abspath(ret["config"])

  if ret["dryrun"]:
    ret["dryrun"] = "True"
  else:
    ret["dryrun"] = "False"

  print("INFO: arg: " + json.dumps(ret, indent=2), file=sys.stderr)
  return ret

def check_arg(arg: Dict[str, str]) -> None:
  if "title" not in arg:
    print("ERROR: command line argument `title` not found", file=sys.stderr)
    exit(1)

  if (len(arg["yyyymmddhhmmss"]) != 14) or (not arg["yyyymmddhhmmss"].isdecimal()):
    print("ERROR: command line option `--yyyymmddhhmmss` is invalid: " + arg["yyyymmddhhmmss"], file=sys.stderr)
    exit(1)

  if not os.path.isfile(arg["config"]):
    print("ERROR: config file: `" + arg["config"] + "` not found", file=sys.stderr)
    exit(1)

