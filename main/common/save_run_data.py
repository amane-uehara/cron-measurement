import os
import json
from common.read_config import apply_template
from common.fetch_run import fetch_run

def save_run_data(data, title, raw_config):
  run  = fetch_run()
  run["hostname"] = raw_config["constant"]["hostname"]
  run["data"] = data

  config = apply_template(raw_config, run["dt"])

  filename = config[title]["save_raw_file"]
  filepath = os.path.dirname(filename)
  os.makedirs(filepath, mode=0o777, exist_ok=True)

  with open(filename, 'w') as f:
    f.write(json.dumps(run))
