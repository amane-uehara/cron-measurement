import sys
import subprocess

def fetch_json(config):
  if "command_list" not in config:
    print("ERROR: command_list not found", file=sys.stderr)
    sys.exit()

  command_list = config["command_list"]
  print("INFO: command_list: " + str(command_list), file=sys.stderr)

  print("INFO: shell begin", file=sys.stderr)
  for command_str in command_list:
    command = subprocess.run(command_str, shell=True, capture_output=True, text=True)
    print(command.stdout, end='', file=sys.stdout)
    print(command.stderr, end='', file=sys.stderr)
  print("INFO: shell end", file=sys.stderr)

  sys.exit()

def key_list():
  return []

if __name__ == "__main__":
  data = fetch_json({
    "command_list":[
      "pwd",
      "ls -l",
      "echo 'today is ${yyyymmdd}'"
      "echo 'now is ${yyyymmddhhmmss}'"
    ]
  })
  print(json.dumps(data))
