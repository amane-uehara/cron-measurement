import bluetooth._bluetooth as bluez
import struct
import binascii
import sys
import json
from math import exp, log

def fetch_json(config):
  mac_addr       = config["sensor_mac_addr"]     # "c8b244000000"
  bt_retry_count = int(config["bt_retry_count"]) # 100
  bt_dev_id      = int(config["bt_dev_id"])      # 0

  sock = bluez.hci_open_dev(bt_dev_id)

  cmd_pkt = struct.pack("<BBBBBBB", 0x01, 0x0, 0x10, 0x0, 0x10, 0x01, 0x00)
  bluez.hci_send_cmd(sock, 0x08, 0x000B, cmd_pkt)

  cmd_pkt = struct.pack("<BB", 0x01, 0x00)
  bluez.hci_send_cmd(sock, 0x08, 0x000C, cmd_pkt)

  flt = bluez.hci_filter_new()
  bluez.hci_filter_all_events(flt)
  bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
  sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)

  data = {}
  for _ in range(bt_retry_count):
    pkt = sock.recv(255)
    if (b'\xd5\x02' not in pkt): continue
    if (b'Rbt' not in pkt): continue
    if (mac_addr != binascii.hexlify((pkt[7:13])[::-1]).decode()): continue

    ( data["temperature"],
      data["relative_humidity"],
      data["ambient_light"],
      data["barometric_pressure"],
      data["sound_noise"],
      data["etvoc"],
      data["eco2"]
    ) = struct.unpack('<hhhlhhh',pkt[23:39])

    t = data['temperature']
    r = data['relative_humidity']
    data['absolute_humidity'] = round(217*6.1078*exp(7.5*(t/100.0)*log(10.0)/((t/100.0)+237.3))/((t/100.0)+273.15)*((r/100.0)/100.0)*100)

    break
  return data

def key_list():
  return [
    "temperature",
    "relative_humidity",
    "absolute_humidity",
    "ambient_light",
    "barometric_pressure",
    "sound_noise",
    "etvoc",
    "eco2"
  ]

if __name__ == "__main__":
  data = fetch_json({
    "mac_addr": "c8b244000000",
    "bt_retry_count": 100,
    "bt_dev_id": 0
  })
  print(json.dumps(data))
