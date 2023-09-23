import unittest
import sys

sys.path.append('../main/')
from common import *
from mock_sensor_data import *

class TestMain(unittest.TestCase):

  def test_trans_to_percentile_json_list(self):
    sensor = mock_import_sensor()

    config = mock_config()
    config["division_number"] = 3

    json_list = [
      mock_run_data_0(),
      mock_run_data_0(),
      mock_run_data_0(),
      mock_run_data_0(),
      mock_run_data_0(),
      mock_run_data_0(),
      mock_run_data_0(),
      mock_run_data_0(),
      mock_run_data_0(),
      mock_run_data_0()
    ]

    json_list[0]["data"]["key_int_0"] = 0
    json_list[1]["data"]["key_int_0"] = 2
    json_list[2]["data"]["key_int_0"] = 4
    json_list[3]["data"]["key_int_0"] = 6
    json_list[4]["data"]["key_int_0"] = 8
    json_list[5]["data"]["key_int_0"] = 1
    json_list[6]["data"]["key_int_0"] = 3
    json_list[7]["data"]["key_int_0"] = 5
    json_list[8]["data"]["key_int_0"] = 7
    json_list[9]["data"]["key_int_0"] = 9

    actual = trans_to_percentile_json_list(json_list, config, sensor["key_list"])

    expected = [
      {"percentile": 0},
      {"percentile": 1},
      {"percentile": 2}
    ]

    expected[0].update(mock_select_list_config_0())
    expected[1].update(mock_select_list_config_0())
    expected[2].update(mock_select_list_config_0())

    expected[0]["data"]["key_int_0"] = 0
    expected[1]["data"]["key_int_0"] = 3
    expected[2]["data"]["key_int_0"] = 6

    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
