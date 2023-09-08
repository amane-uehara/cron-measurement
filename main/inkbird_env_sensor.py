import bluepy
import struct
import sys
import json

def fetch_json(config):
  mac_addr       = config["sensor_mac_addr"]      # "492302f00000"
  bt_retry_count = int(config["bt_retry_count"])  # 100

  mac_short = mac_addr.lower().replace(":","")
  mac_colon = ":".join([mac_short[i:i+2] for i in range(0, len(mac_short), 2)])
  data = {}

  for i in range(bt_retry_count):
    try:
      device = bluepy.btle.Peripheral(mac_colon)
      pkt = device.readCharacteristic(36)
      device.disconnect()

      ( data["temperature"],
        data["humidity"],
        is_sensor_external,
        crc16_modbus
      ) = struct.unpack("<hhBH", pkt)

    except:
      continue
    else:
      break
  return data

def key_list():
  return [
    "temperature",
    "humidity"
  ]

if __name__ == "__main__":
  data = fetch_json({
    "mac_addr": "492302f00000",
    "bt_retry_count": 100
  })
  print(json.dumps(data))
