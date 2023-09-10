import platform
import psutil
import socket
import json
import time
from uuid import getnode

def fetch_json(config):
  resource = {};

  resource["cpu"] = {}
  resource["cpu"]["freq_current"] = psutil.cpu_freq().current
  resource["cpu"]["freq_min"]     = psutil.cpu_freq().min
  resource["cpu"]["freq_max"]     = psutil.cpu_freq().max

  loadavg = psutil.getloadavg()
  resource["cpu"]["loadavg_1"]  = loadavg[0]
  resource["cpu"]["loadavg_5"]  = loadavg[1]
  resource["cpu"]["loadavg_15"] = loadavg[2]
  resource["cpu"]["percent"]    = psutil.cpu_percent(interval=1)

  mem = psutil.virtual_memory()
  resource["mem"] = {}
  resource["mem"]["total"]                 = round(mem.total / 1024.0)
  resource["mem"]["used"]                  = round(mem.used / 1024.0)
  resource["mem"]["free"]                  = round(mem.free / 1024.0)
  resource["mem"]["available"]             = round(mem.available / 1024.0)
  resource["mem"]["buffers"]               = round(mem.buffers / 1024.0)
  resource["mem"]["cached"]                = round(mem.cached / 1024.0)
  resource["mem"]["total_minus_available"] = round((mem.total - mem.available) / 1024.0)
  resource["mem"]["ratio"]                 = round(mem.percent / 100.0, 5) # (total-available)/total

  swap = psutil.swap_memory()
  resource["swap"] = {}
  resource["swap"]["total"] = round(swap.total / 1024.0)
  resource["swap"]["used"]  = round(swap.used / 1024.0)
  resource["swap"]["free"]  = round(swap.free / 1024.0)
  resource["swap"]["ratio"] = round(swap.percent / 100.0, 5)

  disk = psutil.disk_usage("/")
  resource["disk"] = {}
  resource["disk"]["total"] = round(disk.total / 1024.0)
  resource["disk"]["used"]  = round(disk.used / 1024.0)
  resource["disk"]["free"]  = round(disk.free / 1024.0)
  resource["disk"]["ratio"] = round(disk.percent / 100.0, 5)

  network = psutil.net_io_counters()
  resource["network"] = {}
  resource["network"]["bytes_sent"]   = network.bytes_sent
  resource["network"]["bytes_recv"]   = network.bytes_recv
  resource["network"]["packets_sent"] = network.packets_sent
  resource["network"]["packets_recv"] = network.packets_recv
  resource["network"]["errin"]        = network.errin
  resource["network"]["errout"]       = network.errout
  resource["network"]["dropin"]       = network.dropin
  resource["network"]["dropout"]      = network.dropout

  connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  connect_interface.connect(("8.8.8.8", 80))
  resource["network"]["ip_addr"] = connect_interface.getsockname()[0]
  connect_interface.close()

  resource["network"]["mac_addr"] = hex(getnode())[2:]

  resource["uptime"] = {}
  resource["uptime"]["boot_time"] = psutil.boot_time()
  resource["uptime"]["elapsed"]   = int(time.time() - psutil.boot_time())
  resource["uptime"]["users"]     = len(psutil.users())

  resource["sensor"] = {}

  if "cpu_thermal" in psutil.sensors_temperatures():
    t = psutil.sensors_temperatures()["cpu_thermal"]
    if len(t) > 0:
      resource["sensor"]["temperature"] = round(t[0].current * 1000)

  if "coretemp" in psutil.sensors_temperatures():
    t = psutil.sensors_temperatures()["coretemp"]
    if len(t) > 0:
      resource["sensor"]["temperature"] = round(t[0].current * 1000)

  return resource

def key_list():
  return [
    "cpu.freq_current",
    "cpu.freq_min",
    "cpu.freq_max",
    "cpu.loadavg_1",
    "cpu.loadavg_5",
    "cpu.loadavg_15",
    "cpu.percent",
    "mem.total",
    "mem.used",
    "mem.free",
    "mem.available",
    "mem.buffers",
    "mem.cached",
    "mem.total_minus_available",
    "mem.ratio",
    "swap.total",
    "swap.used",
    "swap.free",
    "swap.ratio",
    "disk.total",
    "disk.used",
    "disk.free",
    "disk.ratio",
    "network.bytes_sent",
    "network.bytes_recv",
    "network.packets_sent",
    "network.packets_recv",
    "network.errin",
    "network.errout",
    "network.dropin",
    "network.dropout",
    "network.ip_addr",
    "network.mac_addr",
    "uptime.boot_time",
    "uptime.elapsed",
    "uptime.users",
    "sensor.temperature",
    "sensor.temperature"
  ]

if __name__ == "__main__":
  data = fetch_json()
  print(json.dumps(data))
