import platform
import psutil
import socket
import json
import time
from uuid import getnode

def fetch_json(config):
  resource = {};
  resource["uname"]   = {}
  resource["python"]  = {}
  resource["cpu"]     = {}
  resource["mem"]     = {}
  resource["swap"]    = {}
  resource["disk"]    = {}
  resource["network"] = {}
  resource["uptime"]  = {}
  resource["sensor"]  = {}

  try: uname = platform.uname()
  except: pass
  try: resource["uname"]["system"]    = uname.system
  except: pass
  try: resource["uname"]["node"]      = uname.node
  except: pass
  try: resource["uname"]["release"]   = uname.release
  except: pass
  try: resource["uname"]["version"]   = uname.version
  except: pass
  try: resource["uname"]["machine"]   = uname.machine
  except: pass
  try: resource["uname"]["processor"] = uname.processor
  except: pass

  try: python_build = platform.python_build()
  except: pass
  try: resource["python"]["buildno"]   = python_build[0]
  except: pass
  try: resource["python"]["builddate"] = python_build[1]
  except: pass
  try: resource["python"]["version"]   = platform.python_version()
  except: pass

  try: cpu_freq = psutil.cpu_freq()
  except: pass
  try: resource["cpu"]["freq_current"] = cpu_freq.current
  except: pass
  try: resource["cpu"]["freq_min"]     = cpu_freq.min
  except: pass
  try: resource["cpu"]["freq_max"]     = cpu_freq.max
  except: pass

  try: loadavg = psutil.getloadavg()
  except: pass
  try: resource["cpu"]["loadavg_1"]  = loadavg[0]
  except: pass
  try: resource["cpu"]["loadavg_5"]  = loadavg[1]
  except: pass
  try: resource["cpu"]["loadavg_15"] = loadavg[2]
  except: pass
  try: resource["cpu"]["percent"]    = psutil.cpu_percent(interval=1)
  except: pass

  try: mem = psutil.virtual_memory()
  except: pass
  try: resource["mem"]["total"]                 = round(mem.total / 1024.0)
  except: pass
  try: resource["mem"]["used"]                  = round(mem.used / 1024.0)
  except: pass
  try: resource["mem"]["free"]                  = round(mem.free / 1024.0)
  except: pass
  try: resource["mem"]["available"]             = round(mem.available / 1024.0)
  except: pass
  try: resource["mem"]["buffers"]               = round(mem.buffers / 1024.0)
  except: pass
  try: resource["mem"]["cached"]                = round(mem.cached / 1024.0)
  except: pass
  try: resource["mem"]["total_minus_available"] = round((mem.total - mem.available) / 1024.0)
  except: pass
  try: resource["mem"]["ratio"]                 = round(mem.percent / 100.0, 5) # (total-available)/total
  except: pass

  try: swap = psutil.swap_memory()
  except: pass
  try: resource["swap"]["total"] = round(swap.total / 1024.0)
  except: pass
  try: resource["swap"]["used"]  = round(swap.used / 1024.0)
  except: pass
  try: resource["swap"]["free"]  = round(swap.free / 1024.0)
  except: pass
  try: resource["swap"]["ratio"] = round(swap.percent / 100.0, 5)
  except: pass

  try:
    for part in psutil.disk_partitions(all=True):
      mountpoint = str(part.mountpoint)
      usage = psutil.disk_usage(mountpoint)
      if usage.total == 0:
        continue
      resource["disk"][mountpoint] = {}
      resource["disk"][mountpoint]["fstype"] = str(part.fstype)
      resource["disk"][mountpoint]["total"]  = round(usage.total / 1024.0)
      resource["disk"][mountpoint]["used"]   = round(usage.used / 1024.0)
      resource["disk"][mountpoint]["free"]   = round(usage.free / 1024.0)
      resource["disk"][mountpoint]["ratio"]  = round(usage.percent / 100.0, 5)
  except: pass

  try: network = psutil.net_io_counters()
  except: pass
  try: resource["network"]["bytes_sent"]   = network.bytes_sent
  except: pass
  try: resource["network"]["bytes_recv"]   = network.bytes_recv
  except: pass
  try: resource["network"]["packets_sent"] = network.packets_sent
  except: pass
  try: resource["network"]["packets_recv"] = network.packets_recv
  except: pass
  try: resource["network"]["errin"]        = network.errin
  except: pass
  try: resource["network"]["errout"]       = network.errout
  except: pass
  try: resource["network"]["dropin"]       = network.dropin
  except: pass
  try: resource["network"]["dropout"]      = network.dropout
  except: pass

  try:
    connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connect_interface.connect(("8.8.8.8", 80))
    resource["network"]["ip_addr"] = connect_interface.getsockname()[0]
    connect_interface.close()
  except: pass

  try: resource["network"]["mac_addr"] = hex(getnode())[2:]
  except: pass

  try: resource["uptime"]["boot_time"] = psutil.boot_time()
  except: pass
  try: resource["uptime"]["elapsed"]   = int(time.time() - psutil.boot_time())
  except: pass
  try: resource["uptime"]["users"]     = len(psutil.users())
  except: pass

  try:
    if "cpu_thermal" in psutil.sensors_temperatures():
      t = psutil.sensors_temperatures()["cpu_thermal"]
      if len(t) > 0:
        resource["sensor"]["temperature"] = round(t[0].current * 1000)
    if "coretemp" in psutil.sensors_temperatures():
      t = psutil.sensors_temperatures()["coretemp"]
      if len(t) > 0:
        resource["sensor"]["temperature"] = round(t[0].current * 1000)
  except: pass

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
    "disk./.total",
    "disk./.used",
    "disk./.free",
    "disk./.ratio",
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
