import bluepy
import struct
import sys
import json

def fetch_raw_data(mac_addr, bt_retry_count):
  mac_short = mac_addr.replace(':','')
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
      ) = struct.unpack('<hhBH', pkt)

    except:
      continue
    else:
      break
  return data

if __name__ == "__main__":
  data = fetch_raw_data(sys.argv[1], 100)
  print(json.dumps(data))
