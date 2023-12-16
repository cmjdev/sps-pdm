from pdm_test import *

def test_config():
    # TEST THAT ALL CONFIG VARIABLES EXIST IN CHANNELS
    for i in range(len(channel)):
        assert set(config[i].keys()).issubset(set(channel[i].__dict__.keys())), "CHANNEL MISSING CONFIG VARIABLE"

        for key in config[i].keys():
            assert config[i][key] == getattr(channel[i], key), "MISMATCH BETWEEN CONFIG AND CHANNEL"

def test_command():
    # Test that all commands are entered where they should be
    # TODO: Make this variable based on the total number of channels created
    
    id = BASE_ID + 4
    msg = bytearray([1,2,3,4,5,6,7,8])
    process_command(id, msg)

    expected_results = (1,4,3,8,5,12,7,16)

    j = 0
    for i in range(0,8,2):
        assert channel[j].duty == expected_results[i]
        assert channel[j].freq == expected_results[i+1]
        j += 1
