import os
import sys
import gzip

def save_file(text, config):
  filename = config["save_file"]
  filepath = os.path.dirname(filename)
  os.makedirs(filepath, mode=0o777, exist_ok=True)

  ext = filename.split('.')[-1]
  if ext == "gz":
    with gzip.open(filename, mode='wt') as f:
      f.write(text)
      print("gip file saved: " + filename, end='', file=sys.stderr)

  else:
    with open(filename, 'w') as f:
      f.write(text)
      print("text file saved: " + filename, end='',  file=sys.stderr)

  print(" (" + str(os.path.getsize(filename)) + " byte)", file=sys.stderr)
