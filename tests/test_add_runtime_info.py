import unittest
import sys

sys.path.append('../main/')
from common import *
from mock import *

class TestMain(unittest.TestCase):

  def test_add_runtime_info_0(self):
    sensor = mock_import_sensor()
    config = mock_config()
    data = sensor["fetch_json"]({"mock_type":0})
    expected = add_runtime_info(data, config)
    actual = mock_run_data_0()
    self.assertEqual(expected, actual)

  def test_add_runtime_info_1(self):
    sensor = mock_import_sensor()
    config = mock_config()
    data = sensor["fetch_json"]({"mock_type":1})
    expected = add_runtime_info(data, config)
    actual = mock_run_data_1()
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
