import os
import sys
import argparse
import json
from datetime import datetime

def read_arg():
  now_yyyymmddhhmmss  = datetime.now().strftime("%Y%m%d%H%M%S")

  repository_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  default_config_file = os.path.join(repository_path, "config.json")

  parser = argparse.ArgumentParser()
  parser.add_argument("title", type=str)
  parser.add_argument("--yyyymmddhhmmss", type=str, default=now_yyyymmddhhmmss)
  parser.add_argument("--config", type=str, default=default_config_file)
  parser.add_argument("--dryrun", action='store_true')
  args = parser.parse_args()

  ret = vars(args)
  ret["config_abspath"]  = os.path.abspath(ret["config"])
  ret["config_rawpath"]  = ret["config"]
  ret["repository_path"] = repository_path
  ret["exec_main_py"]    = sys.executable + " " + sys.argv[0]

  del ret["config"]

  print("INFO: arg: " + json.dumps(ret, indent=2), file=sys.stderr)

  if "title" not in ret:
    print("ERROR: command line argument `title` not found", file=sys.stderr)
    exit(1)

  if (len(ret["yyyymmddhhmmss"]) != 14) or (not ret["yyyymmddhhmmss"].isdecimal()):
    print("ERROR: command line option `--yyyymmddhhmmss` is invalid: " + ret["yyyymmddhhmmss"], file=sys.stderr)
    exit(1)

  if not os.path.isfile(ret["config_abspath"]):
    print("ERROR: config file: `" + ret["config_abspath"] + "` not found", file=sys.stderr)
    exit(1)

  return ret
