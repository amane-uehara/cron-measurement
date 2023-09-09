import os
import sys
import argparse
from datetime import datetime

def read_arg():
  now_yyyymmddhhmmss  = datetime.now().strftime("%Y%m%d%H%M%S")

  root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  default_config_file = os.path.join(root_path, "config.json")

  parser = argparse.ArgumentParser()
  parser.add_argument("title", type=str)
  parser.add_argument("--yyyymmddhhmmss", type=str, default=now_yyyymmddhhmmss)
  parser.add_argument("--config", type=str, default=default_config_file)
  args = parser.parse_args()

  ret = vars(args)
  ret["config_abspath"] = os.path.abspath(ret["config"])
  del ret["config"]

  print("INFO: arg: " + str(ret), file=sys.stderr)

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
