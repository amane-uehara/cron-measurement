import psutil
import socket
import json
import time

def fetch_json(config):
  resource = {};

  resource["cpu"] = {}
  resource["cpu"]["core_logical"]  = psutil.cpu_count(logical=True)
  resource["cpu"]["core_physical"] = psutil.cpu_count(logical=False)
  resource["cpu"]["freq_current"]  = psutil.cpu_freq().current
  resource["cpu"]["freq_min"]      = psutil.cpu_freq().min
  resource["cpu"]["freq_max"]      = psutil.cpu_freq().max

  loadavg = psutil.getloadavg()
  resource["cpu"]["loadavg_1"]  = loadavg[0]
  resource["cpu"]["loadavg_5"]  = loadavg[1]
  resource["cpu"]["loadavg_15"] = loadavg[2]
  resource["cpu"]["percent"]    = psutil.cpu_percent(interval=1)

  mem = psutil.virtual_memory()
  resource["mem"] = {}
  resource["mem"]["total"]     = mem.total
  resource["mem"]["used"]      = mem.used
  resource["mem"]["free"]      = mem.free
  resource["mem"]["available"] = mem.available
  resource["mem"]["percent"]   = mem.percent

  swap = psutil.swap_memory()
  resource["swap"] = {}
  resource["swap"]["total"]   = swap.total
  resource["swap"]["used"]    = swap.used
  resource["swap"]["free"]    = swap.free
  resource["swap"]["percent"] = swap.percent

  disk = psutil.disk_usage("/")
  resource["disk"] = {}
  resource["disk"]["total"]   = disk.total
  resource["disk"]["used"]    = disk.used
  resource["disk"]["free"]    = disk.free
  resource["disk"]["percent"] = disk.percent

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

  resource["uptime"] = {}
  resource["uptime"]["boot_time"] = psutil.boot_time()
  resource["uptime"]["elapsed"]   = int(time.time() - psutil.boot_time())
  resource["uptime"]["users"]     = len(psutil.users())

  resource["sensor"] = {"temperature":0}
  if "cpu_thermal" in psutil.sensors_temperatures():
    if psutil.sensors_temperatures()["cpu_thermal"][0]:
      resource["sensor"]["temperature"] = int(psutil.sensors_temperatures()["cpu_thermal"][0].current)

  return resource

def key_list():
  return [
    "cpu.core_logical",
    "cpu.core_physical",
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
    "mem.percent",
    "swap.total",
    "swap.used",
    "swap.free",
    "swap.percent",
    "disk.total",
    "disk.used",
    "disk.free",
    "disk.percent",
    "network.bytes_sent",
    "network.bytes_recv",
    "network.packets_sent",
    "network.packets_recv",
    "network.errin",
    "network.errout",
    "network.dropin",
    "network.dropout",
    "network.ip_addr",
    "uptime.boot_time",
    "uptime.users",
    "sensor.temperature"
  ]

if __name__ == "__main__":
  data = fetch_json()
  print(json.dumps(data))
