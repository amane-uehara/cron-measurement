import sys
from pathlib import Path
SCRIPT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(SCRIPT_ROOT.joinpath('common')))
import read_config
from fetch_raw_data import fetch_raw_data
from save_run_data  import save_run_data

import json
import os

def main(argv):
  title = argv[1]
  raw_config = read_config.read_raw_config(argv)
  data = fetch_raw_data()

  save_run_data(data, title, raw_config)

if __name__ == "__main__":
  main(sys.argv)
  # python3 save_raw_data.py "json_job_title" [--config=/path/to/config.json]
