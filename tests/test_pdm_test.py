from pdm_test import *

def test_config():
    # TEST THAT ALL CONFIG VARIABLES EXIST IN CHANNELS
    for i in range(len(channel)):
        assert set(config[i].keys()).issubset(set(channel[i].__dict__.keys())), "CHANNEL MISSING CONFIG VARIABLE"

        for key in config[i].keys():
            assert config[i][key] == getattr(channel[i], key), "MISMATCH BETWEEN CONFIG AND CHANNEL"

def test_one():
    pass

def test_two():
    pass