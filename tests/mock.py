def mock_config():
  return {
    "yyyymmddhhmmss": "20220304050607",
    "yyyymmdd": "20220304",
    "hostname": "example_host",
    "mac_addr": "1122334455ff",
    "extra": {
      "extra_str": "extra_val",
      "extra_int": 3,
      "extra_bool": True,
      "extra_dict": {
        "foo": "bar"
      }
    },
    "run_key_list": ["dt", "extra.extra_str"],
    "data_key_list": ["key_int_0", "key_dict.key2.key2_1.key2_1_0"]
  }

def mock_raw_data_0():
  return {
    "key_str": "data_0",
    "key_empty": "",
    "key_will_be_ignored": "baz",
    "key_int_0": 0,
    "key_int_1": 1,
    "key_int_-42": -42,
    "key_float_0": 0.0,
    "key_float_11": 1.10,
    "key_float_-42": -42.0,
    "key_bool_true": True,
    "key_bool_false": False,
    "key_empty_dict": {},
    "key_dict": {
      "key0": 0,
      "key1": "one",
      "key2": {
        "key2_0": 21,
        "key2_1": {
          "key2_1_0": 210
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
    "key_float_11",
    "key_float_-42",
    "key_bool_true",
    "key_bool_false",
    "key_empty_dict",
    "key_dict.key0",
    "key_dict.key1",
    "key_dict.key2.key2_0",
    "key_dict.key2.key2_1.key2_1_0"
  ]

def mock_raw_data_1():
  return {
    "key_str": "data_1",
    "key_empty_dict": {},
    "key_dict": {
      "key2": {
        "key2_1": {
          "key2_1_0": 450
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
    "mac_addr": "1122334455ff",
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
      "key_will_be_ignored": "baz",
      "key_int_0": 0,
      "key_int_1": 1,
      "key_int_-42": -42,
      "key_float_0": 0.0,
      "key_float_11": 1.10,
      "key_float_-42": -42.0,
      "key_bool_true": True,
      "key_bool_false": False,
      "key_empty_dict": {},
      "key_dict": {
        "key0": 0,
        "key1": "one",
        "key2": {
          "key2_0": 21,
          "key2_1": {
            "key2_1_0": 210
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
    "mac_addr": "1122334455ff",
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
            "key2_1_0": 450
          }
        }
      }
    }
  }

def mock_json_list():
  return [
    mock_run_data_0(),
    mock_run_data_1(),
  ]

def mock_csv_list_default_key():
  return [
    [
      "20220304050607",
      "20220304",
      "example_host",
      "1122334455ff",
      "data_0",
      "",
      0,
      1,
      -42,
      0.0,
      1.10,
      -42.0,
      True,
      False,
      "",
      0,
      "one",
      21,
      210
    ],[
      "20220304050607",
      "20220304",
      "example_host",
      "1122334455ff",
      "data_1",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      450
    ]
  ]

def mock_csv_list_config_0():
  return [
    "20220304050607",
    "extra_val",
    0,
    210
  ]

def mock_csv_list_config_1():
  return [
    "20220304050607",
    "extra_val",
    "",
    450
  ]

def mock_csv_list_config_key():
  return [
    mock_csv_list_config_0(),
    mock_csv_list_config_1(),
  ]

def mock_select_list_config_0():
  return {
    "dt": "20220304050607",
    "extra": {
      "extra_str": "extra_val"
    },
    "data": {
      "key_int_0": 0,
      "key_dict": {
        "key2": {
          "key2_1": {
            "key2_1_0": 210
          }
        }
      }
    }
  }

def mock_select_list_config_1():
  return {
    "dt": "20220304050607",
    "extra": {
      "extra_str": "extra_val"
    },
    "data": {
      "key_int_0": "",
      "key_dict": {
        "key2": {
          "key2_1": {
            "key2_1_0": 450
          }
        }
      }
    }
  }

def mock_select_list_config_key():
  return [
    mock_select_list_config_0(),
    mock_select_list_config_1(),
  ]
