import json

def fetch_json(config):
  return {}

def key_list():
  return [
    "unixtime",
    "dt_jst9",
    "dt_mac_addr",
    "data.sensor_mac_addr",
    "data.sensor_type",
    "data.temperature",
    "data.relative_humidity",
    "data.absolute_humidity",
    "data.is_sensor_external",
    "data.crc16_modbus",
  ]

if __name__ == "__main__":
  data = fetch_json()
  print(json.dumps(data))
