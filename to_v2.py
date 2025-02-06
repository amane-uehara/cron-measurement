import glob
from datetime import datetime, timezone, timedelta
import gzip
import json
import os

def read_write(input_gz_file, output_gz_file, henkan):
  with gzip.open(input_gz_file, 'rb') as f:
    data = json.load(f)

  w = []
  for d in data:
    if d["data"] == {}:
      continue
    w.append(henkan(d))

  with gzip.open(output_gz_file, 'wb') as f:
    json_str = json.dumps(w, separators=(',', ':'))
    f.write(json_str.encode('utf-8'))

def inkbird_henkan(d):
  return {
    "dt_jst9": d["dt"],
    "http_dongle_mac_addr": d["mac_addr"],
    "unixtime": jst9_to_unixtime(d["dt"]),
    "data": {
      "crc16_modbus": 0,
      "relative_humidity": d["data"]["relative_humidity"],
      "is_sensor_external": 0,
      "absolute_humidity": d["data"]["absolute_humidity"],
      "temperature": d["data"]["temperature"],
    },
    "sensor_type": "inkbird-ibs-th2",
    "sensor_mac_addr": d["extra"]["sensor_mac_addr"].replace(":", "").lower(),
  }

def omron_henkan(d):
  return {
    "dt_jst9": d["dt"],
    "http_dongle_mac_addr": d["mac_addr"],
    "unixtime": jst9_to_unixtime(d["dt"]),
    "data": {
      "sound_noise": d["data"]["sound_noise"],
      "temperature": d["data"]["temperature"],
      "eco2": d["data"]["eco2"],
      "absolute_humidity": d["data"]["absolute_humidity"],
      "ambient_light": d["data"]["ambient_light"],
      "barometric_pressure": d["data"]["barometric_pressure"],
      "etvoc": d["data"]["etvoc"],
      "relative_humidity": d["data"]["relative_humidity"],
    },
    "sensor_type": "omron-2jcie-bu",
    "sensor_mac_addr": d["extra"]["sensor_mac_addr"].replace(":", "").lower(),
  }

def jst9_to_unixtime(jst_str):
  JST = timezone(timedelta(hours=9))
  dt_jst = datetime.strptime(jst_str, "%Y%m%d%H%M%S").replace(tzinfo=JST)
  return int(dt_jst.astimezone(timezone.utc).timestamp())

def main():
  hostname = "raspberry-pi-3-*****"

  input_gz_file_list = glob.glob(f"~/data_v2/daily/{hostname}/inkbird_env_sensor/all_json/*.gz")
  for input_gz_file in input_gz_file_list:
    filename = os.path.basename(input_gz_file)
    output_gz_file = f"~/data_v2/daily/{hostname}/inkbird_env_sensor_v2/all_json/{filename}"
    print(input_gz_file, output_gz_file)
    read_write(input_gz_file, output_gz_file, inkbird_henkan)

  input_gz_file_list = glob.glob(f"~/data_v2/daily/{hostname}/omron_env_sensor/all_json/*.gz")
  for input_gz_file in input_gz_file_list:
    filename = os.path.basename(input_gz_file)
    output_gz_file = f"~/data_v2/daily/{hostname}/omron_env_sensor_v2/all_json/{filename}"
    print(input_gz_file, output_gz_file)
    read_write(input_gz_file, output_gz_file, omron_henkan)

main()
