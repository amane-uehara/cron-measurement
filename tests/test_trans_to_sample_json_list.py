import unittest
import sys

sys.path.append('../main/')
from common import *
from mock import *

class TestMain(unittest.TestCase):

  def test_trans_to_sample_json_list(self):
    sensor    = mock_import_sensor()

    config    = mock_config()
    config["sample_time_key"] = "dt"
    config["sample_begin"] = "20221229000000"
    config["sample_end"]   = "20221229030000"
    config["sample_interval"] = "3600"

    json_list = [
      mock_run_data_0(),
      mock_run_data_1(),
      mock_run_data_0(),
      mock_run_data_1(),
      mock_run_data_0(),
      mock_run_data_1(),
      mock_run_data_0(),
      mock_run_data_1(),
      mock_run_data_0(),
      mock_run_data_1()
    ]

    json_list[0]["dt"] = "20221229000000"
    json_list[1]["dt"] = "20221229005900"
    json_list[2]["dt"] = "20221229010000"
    json_list[3]["dt"] = "20221229010100"
    json_list[4]["dt"] = "20221229015900"
    json_list[5]["dt"] = "20221229020000"
    json_list[6]["dt"] = "20221229020100"
    json_list[7]["dt"] = "20221229025900"
    json_list[8]["dt"] = "20221229030000"
    json_list[9]["dt"] = "20221229030100"

    expected  = trans_to_sample_json_list(json_list, config)

    actual = [
      mock_run_data_0(),
      mock_run_data_0(),
      mock_run_data_1()
    ]

    actual[0]["dt"] = "20221229000000"
    actual[1]["dt"] = "20221229010000"
    actual[2]["dt"] = "20221229020000"

    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
