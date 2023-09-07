import sys
import json
from datetime import datetime
from uuid import getnode as get_mac

def fetch_run():
  ret = {}
  ret['dt']  = datetime.now().strftime("%Y%m%d%H%M%S")
  ret['mac_addr'] = hex(get_mac())[2:]

  return ret

if __name__ == "__main__":
  data = fetch_raw_system_resource.fetch_data()
  run  = fetch_run()
  run["data"] = data
  print(json.dumps(run))
