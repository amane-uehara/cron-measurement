import platform
import psutil
import socket
import json
import time
from uuid import getnode

def fetch_json(config):
  resource = {};

  uname = platform.uname()

  resource["uname"] = {}
  resource["uname"]["system"]    = uname.system
  resource["uname"]["node"]      = uname.node
  resource["uname"]["release"]   = uname.release
  resource["uname"]["version"]   = uname.version
  resource["uname"]["machine"]   = uname.machine
  resource["uname"]["processor"] = uname.processor

  resource["python"] = {}
  python_build = platform.python_build()
  resource["python"]["buildno"]   = python_build[0]
  resource["python"]["builddate"] = python_build[1]
  resource["python"]["version"]   = platform.python_version()

  resource["cpu"] = {}
  resource["cpu"]["core_logical"]  = psutil.cpu_count(logical=True)
  resource["cpu"]["core_physical"] = psutil.cpu_count(logical=False)
  resource["cpu"]["freq_min"]      = psutil.cpu_freq().min
  resource["cpu"]["freq_max"]      = psutil.cpu_freq().max

  mem = psutil.virtual_memory()
  resource["mem"] = {}
  resource["mem"]["total"] = round(mem.total / 1024.0)

  disk = psutil.disk_usage("/")
  resource["disk"] = {}
  resource["disk"]["total"] = round(disk.total / 1024.0)

  resource["uptime"] = {}
  resource["uptime"]["boot_time"] = psutil.boot_time()

  resource["network"] = {}
  connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  connect_interface.connect(("8.8.8.8", 80))
  resource["network"]["ip_addr"] = connect_interface.getsockname()[0]
  connect_interface.close()

  resource["network"]["mac_addr"] = hex(getnode())[2:]

  return resource

def key_list():
  return [
    "uname.system",
    "uname.node",
    "uname.release",
    "uname.version",
    "uname.machine",
    "uname.processor",
    "python.buildno",
    "python.builddate",
    "python.version",
    "cpu.core_logical",
    "cpu.core_physical",
    "cpu.freq_min",
    "cpu.freq_max",
    "mem.total",
    "disk.total",
    "uptime.boot_time",
    "network.ip_addr",
    "network.mac_addr"
  ]

if __name__ == "__main__":
  data = fetch_json()
  print(json.dumps(data))
