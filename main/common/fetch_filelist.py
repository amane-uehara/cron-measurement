import sys
from glob import glob

def fetch_filelist(glob_filelist):
  ret = []
  for glob_file in glob_filelist:
    ret += glob(glob_file)
  ret.sort()
  print("filelist: " + str(ret), file=sys.stderr)
  return ret
