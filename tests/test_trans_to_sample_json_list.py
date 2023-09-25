import unittest
import sys

sys.path.append('../main/')
from common import *
from mock_sensor_data import *

class TestMain(unittest.TestCase):

  def setUp(self):
    self.json_list = [
      {"a":0, "dt": "20111111000000"},
      {"a":1, "dt": "20111111005900"},
      {"a":2, "dt": "20111111010000"},
      {"a":3, "dt": "20111111010100"},
      {"a":4, "dt": "20111111015900"},
      {"a":5, "dt": "20111111020000"},
      {"a":6, "dt": "20111111020100"},
      {"a":7, "dt": "20111111025900"},
      {"a":8, "dt": "20111111030000"},
      {"a":9, "dt": "20111111030100"}
    ]

  def test_trans_to_sample_json_list_0(self):
    config = {}
    config["sample_time_key"] = "dt"
    config["sample_begin"]    = "20000101000000"
    config["sample_end"]      = "20000101030000"
    config["sample_interval"] = "3600"
    actual = trans_to_sample_json_list(self.json_list, config)

    expected = []

    self.assertEqual(expected, actual)

  def test_trans_to_sample_json_list_1(self):
    config = {}
    config["sample_time_key"] = "dt"
    config["sample_begin"]    = "30000101000000"
    config["sample_end"]      = "30000101030000"
    config["sample_interval"] = "3600"
    actual = trans_to_sample_json_list(self.json_list, config)

    expected = []

    self.assertEqual(expected, actual)

  def test_trans_to_sample_json_list_2(self):
    config = {}
    config["sample_time_key"] = "dt"
    config["sample_begin"]    = "20111111000000"
    config["sample_end"]      = "20111111030000"
    config["sample_interval"] = "3600"
    actual = trans_to_sample_json_list(self.json_list, config)

    expected = [
      {"a":0, "dt": "20111111000000"},
      {"a":2, "dt": "20111111010000"},
      {"a":5, "dt": "20111111020000"}
    ]

    self.assertEqual(expected, actual)

  def test_trans_to_sample_json_list_3(self):
    config = {}
    config["sample_time_key"] = "dt"
    config["sample_begin"]    = "20111111000001"
    config["sample_end"]      = "20111111030000"
    config["sample_interval"] = "3600"
    actual = trans_to_sample_json_list(self.json_list, config)

    expected = [
      {"a":1, "dt": "20111111005900"},
      {"a":3, "dt": "20111111010100"},
      {"a":6, "dt": "20111111020100"}
    ]

    self.assertEqual(expected, actual)

  def test_trans_to_sample_json_list_4(self):
    config = {}
    config["sample_time_key"] = "dt"
    config["sample_begin"]    = "20111111000000"
    config["sample_end"]      = "20111111025959"
    config["sample_interval"] = "3600"
    actual = trans_to_sample_json_list(self.json_list, config)

    expected = [
      {"a":0, "dt": "20111111000000"},
      {"a":2, "dt": "20111111010000"},
      {"a":5, "dt": "20111111020000"}
    ]

    self.assertEqual(expected, actual)

  def test_trans_to_sample_json_list_5(self):
    config = {}
    config["sample_time_key"] = "dt"
    config["sample_begin"]    = "20111111000000"
    config["sample_end"]      = "20111111030001"
    config["sample_interval"] = "3600"
    actual = trans_to_sample_json_list(self.json_list, config)

    expected = [
      {"a":0, "dt": "20111111000000"},
      {"a":2, "dt": "20111111010000"},
      {"a":5, "dt": "20111111020000"},
      {"a":8, "dt": "20111111030000"}
    ]

    self.assertEqual(expected, actual)

  def test_trans_to_sample_json_list_6(self):
    config = {}
    config["sample_time_key"] = "dt"
    config["sample_begin"]    = "30111111000000"
    config["sample_end"]      = "30111111000010"
    config["sample_interval"] = "1"
    actual = trans_to_sample_json_list(self.json_list, config)

    expected = [
    ]

    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
