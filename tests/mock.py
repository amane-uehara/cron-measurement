def mock_config():
  return {
    "yyyymmddhhmmss": "20220304050607",
    "yyyymmdd": "20220304",
    "hostname": "example_host",
    "mac_addr": "11:22:33:44:55:FF",
    "extra": {
      "extra_str": "extra_val",
      "extra_int": 3,
      "extra_bool": True,
      "extra_dict": {
        "foo": "bar"
      }
    }
  }

def mock_raw_data_0():
  return {
    "key_str": "data_0",
    "key_empty": "",
    "key_int_0": 0,
    "key_int_1": 1,
    "key_int_-42": -42,
    "key_float_0": 0.0,
    "key_float_1.1": 1.10,
    "key_float_-42": -42.0,
    "key_bool_true": True,
    "key_bool_false": False,
    "key_empty": "",
    "key_empty_dict": {},
    "key_dict": {
      "key0": 0,
      "key1": "one",
      "key2": {
        "key2_0": 21,
        "key2_1": {
          "key_2_1_0": 210
        }
      }
    }
  }

def mock_key_list():
  return [
    "key_str",
    "key_empty",
    "key_int_0",
    "key_int_1",
    "key_int_-42",
    "key_float_0",
    "key_float_1.1",
    "key_float_-42",
    "key_bool_true",
    "key_bool_false",
    "key_empty",
    "key_empty_dict",
    "key_dict",
    "key_dict.key0",
    "key_dict.key1",
    "key_dict.key2",
    "key_dict.key2.key2_0",
    "key_dict.key2.key2_1",
    "key_dict.key2.key2_1.key_2_1_0"
  ]

def mock_raw_data_1():
  return {
    "key_str": "data_1",
    "key_empty_dict": {},
    "key_dict": {
      "key2": {
        "key2_1": {
          "key_2_1_0": 450
        }
      }
    }
  }

def mock_import_sensor():
  ret = {}
  ret["fetch_json"] = mock_fetch_json
  ret["key_list"]   = mock_key_list()
  return ret

def mock_fetch_json(config):
  if config["mock_type"] == 0:
    return mock_raw_data_0()
  elif config["mock_type"] == 1:
    return mock_raw_data_1()
  else:
    return {}

def mock_run_data_0():
  return {
    "dt": "20220304050607",
    "yyyymmdd": "20220304",
    "hostname": "example_host",
    "mac_addr": "11:22:33:44:55:FF",
    "extra": {
      "extra_str": "extra_val",
      "extra_int": 3,
      "extra_bool": True,
      "extra_dict": {
        "foo": "bar"
      }
    },
    "data": {
      "key_str": "data_0",
      "key_empty": "",
      "key_int_0": 0,
      "key_int_1": 1,
      "key_int_-42": -42,
      "key_float_0": 0.0,
      "key_float_1.1": 1.10,
      "key_float_-42": -42.0,
      "key_bool_true": True,
      "key_bool_false": False,
      "key_empty": "",
      "key_empty_dict": {},
      "key_dict": {
        "key0": 0,
        "key1": "one",
        "key2": {
          "key2_0": 21,
          "key2_1": {
            "key_2_1_0": 210
          }
        }
      }
    }
  }

def mock_run_data_1():
  return {
    "dt": "20220304050607",
    "yyyymmdd": "20220304",
    "hostname": "example_host",
    "mac_addr": "11:22:33:44:55:FF",
    "extra": {
      "extra_str": "extra_val",
      "extra_int": 3,
      "extra_bool": True,
      "extra_dict": {
        "foo": "bar"
      }
    },
    "data": {
      "key_str": "data_1",
      "key_empty_dict": {},
      "key_dict": {
        "key2": {
          "key2_1": {
            "key_2_1_0": 450
          }
        }
      }
    }
  }
