def mock_arg_replace_test():
  return {
    "title": "config_title_0",
    "yyyymmddhhmmss": "20220304050607",
    "config": "/path/to/repo_path/config.json",
    "dryrun": "False",
    "current_path": "/path/to/current_path",
    "repository_path": "/path/to/repo_path",
    "default_config_file": "/path/to/repo_path/config.json",
    "sys_executable": "/usr/bin/python3",
    "now_yyyymmddhhmmss": "20300101010101",
    "mac_addr": "1122334455ff",
    "exec_main_py": "/usr/bin/python3 main/main.py",
    "config_abspath": "/path/to/repo_path/config.json"
  }

def mock_raw_config_replace_test():
  return {
    "constant": {
      "hostname": "example_host",
      "2_day_before": "${yyyymmdd-2}",
      "10_hour_after": "${yyyymmddhh+10}",
      "aaa": "AAA",
      "bbb": "will_be_overwritten_by_BBB",
      "will_be_DDD": "${ddd}",
      "will_be_XXX_1": "${xxx}",
      "will_be_XXX_3": "${will_be_XXX_2}",
      "no_replace_zzz_1": "${zzz}"
    },
    "config_title_0": {
      "bbb": "BBB",
      "will_be_AAA": "${aaa}",
      "will_be_BBB": "${bbb}",
      "will_be_CCC": "${ccc}",
      "will_be_long": "hoge${aaa}piyo${bbb}${ccc}fuga",
      "ccc": "CCC",
      "ddd": "DDD",
      "xxx": "XXX",
      "will_be_XXX_2": "${will_be_XXX_1}",
      "will_be_XXX_4": "${will_be_XXX_3}",
      "dict": {
        "zzz": "ZZZ",
        "will_be_AAA": "${aaa}"
      },
      "no_replace_zzz": "${zzz}",
      "list": ["${aaa}", "${zzz}"]
    }
  }

def mock_config_replace_test():
  return {
    "bbb": "BBB",
    "will_be_AAA": "AAA",
    "will_be_BBB": "BBB",
    "will_be_CCC": "CCC",
    "will_be_long": "hogeAAApiyoBBBCCCfuga",
    "ccc": "CCC",
    "ddd": "DDD",
    "xxx": "XXX",
    "will_be_XXX_2": "XXX",
    "will_be_XXX_4": "XXX",
    "dict": {
      "zzz": "ZZZ",
      "will_be_AAA": "AAA"
    },
    "no_replace_zzz": "${zzz}",
    "list": ["AAA", "${zzz}"],
    "hostname": "example_host",
    "2_day_before": "20220302",
    "10_hour_after": "2022030415",
    "aaa": "AAA",
    "will_be_DDD": "DDD",
    "will_be_XXX_1": "XXX",
    "will_be_XXX_3": "XXX",
    "no_replace_zzz_1": "${zzz}",
    "yyyymmddhhmmss": "20220304050607",
    "yyyymmddhhmm": "202203040506",
    "yyyymmddhh": "2022030405",
    "yyyymmdd": "20220304",
    "yyyymm": "202203",
    "yyyy": "2022",
    "repository_path": "/path/to/repo_path",
    "dryrun": "False",
    "fork_main_py": "/usr/bin/python3 main/main.py --config /path/to/repo_path/config.json",
    "mac_addr": "1122334455ff",
    "hostname": "example_host"
  }

# ----------------------------------------------------------------------------------------------------

def mock_arg_exec_test():
  return {
    "title": "config_title_1",
    "yyyymmddhhmmss": "20220304050607",
    "config": "./config.json",
    "dryrun": "True",
    "current_path": "/path/to/current_path",
    "repository_path": "/path/to/repo_path",
    "default_config_file": "/path/to/repo_path/config.json",
    "sys_executable": "/usr/bin/python3",
    "now_yyyymmddhhmmss": "20300101010101",
    "mac_addr": "1122334455ff",
    "exec_main_py": "/usr/bin/python3 main/main.py",
    "config_abspath": "/path/to/repo_path/config.json"
  }

def mock_raw_config_exec_test():
  return {
    "constant": {
      "hostname": "example_host",
    },
    "config_title_0": {
      "will_be": "igonred"
    },
    "config_title_1": {
      "exec": "${fork_main_py} foobar --yyyymmddhhmmss: ${yyyymmddhh-1}0000" 
    },
    "config_title_2": {
      "will_be": "igonred"
    }
  }

def mock_config_exec_test():
  return {
    "exec": "/usr/bin/python3 main/main.py --config /path/to/repo_path/config.json --dryrun foobar --yyyymmddhhmmss: 20220304040000",
    "hostname": "example_host",
    "yyyymmddhhmmss": "20220304050607",
    "yyyymmddhhmm": "202203040506",
    "yyyymmddhh": "2022030405",
    "yyyymmdd": "20220304",
    "yyyymm": "202203",
    "yyyy": "2022",
    "repository_path": "/path/to/repo_path",
    "dryrun": "True",
    "fork_main_py": "/usr/bin/python3 main/main.py --config /path/to/repo_path/config.json --dryrun",
    "mac_addr": "1122334455ff",
    "hostname": "example_host"
  }
