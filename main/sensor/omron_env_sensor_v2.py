import json

def fetch_json(config):
  return {}

def key_list():
  return [
    "unixtime",
    "dt_jst9",
    "http_dongle_mac_addr",
    "data.sensor_mac_addr",
    "data.sensor_type",
    "data.temperature",
    "data.relative_humidity",
    "data.absolute_humidity",
    "data.ambient_light",
    "data.barometric_pressure",
    "data.sound_noise",
    "data.etvoc",
    "data.eco2",
  ]

if __name__ == "__main__":
  data = fetch_json()
  print(json.dumps(data))
