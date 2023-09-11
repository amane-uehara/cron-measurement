import sys
import json
import gzip
from glob import glob

def fetch_json_list(config):
  input_file_list = fetch_filelist(config["input_file_list"])
  print("INFO: input file list[0]:  " + input_file_list[0], file=sys.stderr)
  print("INFO: input file list[-1]: " + input_file_list[-1], file=sys.stderr)
  print("INFO: number of input files: " + str(len(input_file_list)), file=sys.stderr)

  join_list = []

  for filename in input_file_list:
    ext = filename.split(".")[-1]
    if ext == "gz":
      with gzip.open(filename, 'r') as f:
        json_data = json.load(f)
        if isinstance(json_data, dict):
          join_list.append(json_data)
        if isinstance(json_data, list):
          join_list += json_data
    else:
      with open(filename, "r") as f:
        json_data = json.load(f)
        if isinstance(json_data, dict):
          join_list.append(json_data)
        if isinstance(json_data, list):
          join_list += json_data

  sorted_list = sorted(join_list, key=custom_sort)
  print("INFO: input json list length: " + str(len(sorted_list)), file=sys.stderr)

  return sorted_list

def fetch_filelist(glob_filelist):
  ret = []
  for glob_file in glob_filelist:
    ret += glob(glob_file)
  ret.sort()
  return ret

def custom_sort(item):
  if "dt" in item:
    dt = item["dt"]
  else:
    dt = ""

  if "mac_addr" in item:
    mac_addr = item["mac_addr"]
  else:
    mac_addr = ""

  return (dt, mac_addr)
