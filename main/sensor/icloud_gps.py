from pyicloud import PyiCloudService
import sys

def fetch_json(config):
  apple_id = config["apple_id"]
  password = config["password"]
  cookie_directory = config["cookie_directory"]

  api = PyiCloudService(apple_id=apple_id, password=password, cookie_directory=cookie_directory)
  login_session(api)
  # location = api.devices[0].location()
  location = api.iphone.location()
  return location

def login_session(api):
  if api.requires_2fa:
    print('Two-factor authentication required.', file=sys.stderr)
    code = input('Enter the code you received of one of your approved devices: ')
    result = api.validate_2fa_code(code)
    print('Code validation result: {}'.format(result), file=sys.stderr)

    if not result:
      print('Failed to verify security code', file=sys.stderr)
      sys.exit(1)

    if not api.is_trusted_session:
      print('Session is not trusted. Requesting trust...', file=sys.stderr)
      result = api.trust_session()
      print('Session trust result {}'.format(result), file=sys.stderr)

    if not result:
      print('Failed to request trust. You will likely be prompted for the code again in the coming weeks', file=sys.stderr)

def key_list():
  return [
    "timeStamp",
    "latitude",
    "longitude",
    "horizontalAccuracy",
    "verticalAccuracy",
    "isOld",
    "isInaccurate",
    "locationFinished",
    "locationType",
    "locationMode",
    "secureLocation",
    "secureLocationTs",
    "floorLevel",
    "altitude",
    "positionType"
  ]

if __name__ == "__main__":
  data = fetch_json({
    "apple_id": "xxx.xxx@xxx.xx",
    "password": "xxxxxxxxxxx",
    "cookie_directory": "/path/to/somewhere"
  })
  print(str(data))
