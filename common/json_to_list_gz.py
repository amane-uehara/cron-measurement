import sys
from pathlib import Path
SCRIPT_ROOT = Path(__file__).resolve().parent.parent

import os
from glob import glob
import json
import gzip

from read_config import read_config
from time_list import time_list

def main(argv):
  title = argv[1]
  config_filename = str(SCRIPT_ROOT.joinpath('config.json'))
  if len(argv) >= 6: config_filename = argv[5]

  for yyyymmddhhmmss in time_list(argv[2], argv[3], argv[4]):
    print(yyyymmddhhmmss)
    config = read_config(config_filename, yyyymmddhhmmss)

    load_file_list = glob(config[title]["load_json_files"])
    print(list(load_file_list))
    if not load_file_list: continue

    save_file = config[title]["save_json_gz_file"]
    save_path = os.path.dirname(save_file)
    os.makedirs(save_path, mode=0o777, exist_ok=True)

    join_data = []
    for load_file in load_file_list:
      with open(load_file, 'r') as f:
        join_data.append(json.load(f))
    print(list(join_data))

    with gzip.open(save_file, mode='wt') as f:
      f.write(json.dumps(join_data))
    return 0

if __name__ == "__main__":
  main(sys.argv)
  # python3 save_raw_data.py "system_resource_daily" 20230905000000 20230906000000 86400 [/path/to/config.json]
