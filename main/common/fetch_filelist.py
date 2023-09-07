from glob import glob

def fetch_filelist(glob_template):
  return sorted(glob(glob_template))
