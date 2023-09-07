import bluetooth._bluetooth as bluez
import struct
import binascii
import sys
import json
from math import exp, log

def fetch_json(mac_addr, bt_retry_count, bt_dev_id):
  mac_addr_lower = mac_addr.lower().replace(':','')
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
    if (mac_addr_lower != binascii.hexlify((pkt[7:13])[::-1]).decode()): continue

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

if __name__ == "__main__":
  data = fetch_json(sys.argv[1], 100, 0)
  print(json.dumps(data))
