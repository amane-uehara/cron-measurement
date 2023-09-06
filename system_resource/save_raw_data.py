import sys
from pathlib import Path
SCRIPT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(SCRIPT_ROOT.joinpath('common')))
from fetch_run import fetch_run
import read_config
from fetch_raw_data import fetch_raw_data

import json
import os

def main(argv):
  title = argv[1]
  raw_config = read_config.read_raw_config(argv)

  data = fetch_raw_data()
  run  = fetch_run()
  run["hostname"] = raw_config["constant"]["hostname"]
  run["data"] = data

  config = read_config.apply_template(raw_config, run["dt"])

  filename  = config[title]["save_raw_file"]
  filepath  = os.path.dirname(filename)
  os.makedirs(filepath, mode=0o777, exist_ok=True)

  with open(filename, 'w') as f:
    f.write(json.dumps(run))

if __name__ == "__main__":
  main(sys.argv)
  # python3 save_raw_data.py "system_resource" [--config=/path/to/config.json]
