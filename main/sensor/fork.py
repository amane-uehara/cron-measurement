import sys
import subprocess

def fetch_json(config):
  fork_main_py = config["fork_main_py"]

  if "job_list" not in config:
    print("ERROR: job_list not found", file=sys.stderr)
    sys.exit()

  job_list = config["job_list"]
  print("INFO: job_list: " + str(job_list), file=sys.stderr)

  opt_time = "--yyyymmddhhmmss "
  if "fork_time" in config:
    opt_time += config["fork_time"]
  else:
    opt_time += config["yyyymmddhhmmss"]

  print("INFO: shell begin", file=sys.stderr)
  for job in job_list:
    command_str = fork_main_py + " " + opt_time + " " + job
    print("$ " + command_str, file=sys.stderr)
    command = subprocess.run(command_str, shell=True, capture_output=True, text=True)
    print(command.stdout, end='', file=sys.stdout)
    print(command.stdout, end='', file=sys.stderr)
    print(command.stderr, end='', file=sys.stderr)
  print("INFO: shell end", file=sys.stderr)

  sys.exit()

def key_list():
  return []

if __name__ == "__main__":
  data = fetch_json({
    "fork_main_py": "python3 main/main.py",
    "fork_time": "20000101000000",
    "job_list":[
      "pwd",
      "ls -l",
      "echo 'today is ${yyyymmdd}'"
      "echo 'now is ${yyyymmddhhmmss}'"
    ]
  })
  print(json.dumps(data))
