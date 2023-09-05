import json
import os
import sys
from datetime import datetime

from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(SCRIPT_ROOT.joinpath('common')))

import fetch_run
import read_config
import fetch_raw_data

def main(argv):
  title = argv[1]

  yyyymmddhhmmss = datetime.now().strftime("%Y%m%d%H%M%S")
  config_filename = str(SCRIPT_ROOT.joinpath('config.json'))
  if len(argv) >= 3: config_filename = argv[2]
  config = read_config.read_config(config_filename, yyyymmddhhmmss)

  data = fetch_raw_data.fetch_raw_data()
  run  = fetch_run.fetch_run()
  run["hostname"] = config["constant"]["hostname"]
  run["data"] = data

  filename  = config[title]["save_raw_file"]
  filepath  = os.path.dirname(filename)
  os.makedirs(filepath, mode=0o777, exist_ok=True)

  with open(filename, 'w') as f:
    f.write(json.dumps(run))

if __name__ == "__main__":
  main(sys.argv)
  # python3 save_raw_data.py "system_resource" [/path/to/config.json]
