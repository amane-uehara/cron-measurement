import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import os

_SAVE_PATH_ = None

def save_file(data):
  dt = data["dt_jst9"]
  sensor_type = data["sensor_type"]
  sensor_addr = data["sensor_mac_addr"]
  dongle_addr = data["dt_mac_addr"]
  filename = f"{dt}_{dongle_addr}_{sensor_addr}_{sensor_type}.json"
  filepath = os.path.join(_SAVE_PATH_, filename)

  os.makedirs(_SAVE_PATH_, exist_ok=True)
  with open(filepath, "w", encoding="utf-8") as f:
    f.write(json.dumps(data, separators=(',',':')))

class SingleRequestHandler(BaseHTTPRequestHandler):
  global _SAVE_PATH_
  def do_POST(self):
    content_length = int(self.headers.get("Content-Length", 0))
    post_data = self.rfile.read(content_length) if content_length > 0 else b""

    data_dict = json.loads(post_data.decode("utf-8"))
    print("Received:", data_dict)

    for d in data_dict:
      save_file(d)

    self.send_response(200)
    self.send_header("Content-Type", "text/plain; charset=utf-8")
    self.end_headers()
    self.wfile.write(b"OK\n")

def fetch_json(config):
  global _SAVE_PATH_
  _SAVE_PATH_ = config["save_path"]    # /mnt/ramdisk/sensor
  ip          = config["ip"]           # "0.0.0.0"
  port        = int(config["port"])    # 5000
  timeout     = int(config["timeout"]) # 5

  server = HTTPServer((ip, port), SingleRequestHandler)
  server.socket.settimeout(timeout)

  try:
    print(f"Waiting for one POST request (or timeout in {timeout}s)...")
    server.handle_request()
  except socket.timeout:
    print(f"No requests arrived within {timeout} seconds. Shutting down.")
  finally:
    server.server_close()
    print("Server closed.")
  sys.exit()

def key_list():
  return []

if __name__ == "__main__":
  data = fetch_json({})
