import unittest
import sys

sys.path.append('../main/')
from common import *
from mock_sensor_data import *

class TestMain(unittest.TestCase):

  def test_trans_to_list_list___config_key(self):
    sensor    = mock_import_sensor()
    config    = mock_config()
    json_list = mock_json_list()
    expected  = trans_to_list_list(json_list, config, sensor["key_list"])
    actual    = mock_csv_list_config_key()
    self.assertEqual(expected, actual)

  def test_trans_to_list_list___default_key(self):
    sensor    = mock_import_sensor()
    config    = mock_config()
    json_list = mock_json_list()
    del config["run_key_list"]
    del config["data_key_list"]
    expected  = trans_to_list_list(json_list, config, sensor["key_list"])
    actual    = mock_csv_list_default_key()
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
