from glob import glob
import os

def fetch_sensor_list():
  main_path   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  sensor_path = os.path.join(main_path, "sensor", "*.py")
  sensor_file_list = glob(sensor_path)
  sensor_name_list = list(map(lambda x: str(os.path.basename(x))[:-3], sensor_file_list))
  print(sensor_name_list)
  #load_file_list = fetch_filelist(config["load_file_list"])
  #print('abs dirname: ', os.path.dirname(os.path.abspath(__file__)))

  #join_list = []
  #for json_file in load_file_list:
  #  with open(json_file, "r") as f:
  #    json_data = json.load(f)
  #    if isinstance(json_data, dict):
  #      join_list.append(json_data)
  #    if isinstance(json_data, list):
  #      join_list += json_data

  #sorted_list = sorted(join_list, key=custom_sort)
  #return sorted_list
