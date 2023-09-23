import unittest
import sys

sys.path.append('../main/')
from common import *
from mock_config import *

class TestMain(unittest.TestCase):

  def test_join_arg_config(self):
    arg        = mock_arg_replace_test()
    raw_config = mock_raw_config_replace_test()
    expected   = join_arg_config(arg, raw_config)
    actual     = mock_config_replace_test()
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
