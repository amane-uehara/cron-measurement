import sys
import os
from glob import glob
import json

from common.read_config import read_raw_config, apply_template
from common.time_list import time_list
from common.fetch_filelist import fetch_filelist

def json_to_list(config):
  with open(load_file, 'r') as f:
    join_data.append(json.load(f))

  return join_data

if __name__ == "__main__":
  print(list(join_data), file=sys.stderr)
  data = main(sys.argv)
  # python3 save_raw_data.py "system_resource_daily" 20230905000000 20230906000000 [--config=/path/to/config.json]
