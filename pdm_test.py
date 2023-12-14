import json
import time
from channel import Channel

with open("config.json") as f:
    config = json.load(f)

message = bytearray(8)

# ci Stores the byte index, offsets and masks for channel feedback
# Byte Index(0), Shutdown Offset(1), Shutdown Mask(2), Status Offset(3), Status Mask(4), Active Offset(5), Status Offset(6)
ci = [
    (4, 7, 128, 5, 96, 4, 16),
    (4, 3, 1, 1, 6, 0, 1),
    (5, 7, 128, 5, 96, 4, 16),
    (5, 3, 1, 1, 6, 0, 1),
]

BASE_ID = 0x666

# DEFINES
SHUTDOWN_OFFSET = 1
SHUTDOWN_MASK = 2
STATUS_OFFSET = 3
STATUS_MASK = 4
ACTIVE_OFFSET = 5
ACTIVE_MASK = 6

# FLAGS
STATUS_OFF = 0
STATUS_ACTIVE = 1
STATUS_UNDER_CURRENT = 2
STATUS_OVER_CURRENT = 3


def set_mask(channel, value, offset, mask):
    if channel % 2:  # Even Channels
        message[ci[channel][0]] = message[ci[channel][0]] & ~ci[channel][mask]
        message[ci[channel][0]] = message[ci[channel][0]] | value << ci[channel][offset]
    else:  # Odd Channels
        message[ci[channel][0]] = message[ci[channel][0]] & ~ci[channel][mask]
        message[ci[channel][0]] = message[ci[channel][0]] | value << ci[channel][offset]


def send_feedback():
    base = BASE_ID
    for i, c in enumerate(channel):
        ch = i % 4

        # set current
        message[ch] = int(c.current / 50)

        # set shutdown
        set_mask(ch, c.shutdown, SHUTDOWN_OFFSET, SHUTDOWN_MASK)

        # set s1tatus
        set_mask(ch, c.status, STATUS_OFFSET, STATUS_MASK)

        # set active
        set_mask(ch, c.active, ACTIVE_OFFSET, ACTIVE_MASK)

        if ch == 3:
            print(hex(base), message)
            base = base + 1


channel = [
    Channel(
        fuse_min=config[i]["fuse_min"],
        fuse_max=config[i]["fuse_max"],
        fuse_inrush=config[i]["fuse_inrush"],
        fuse_delay=config[i]["fuse_delay"],
        soft_start=config[i]["soft_start"],
        retry_delay=config[i]["retry_delay"],
        pwm_mode=config[i]["pwm_mode"],
    )
    for i in range(4)
]


# SET UP FEEDBACK MESSAGE 20Hz?


def process_config(msg):
    pass  # channel[msg.id - base_id + 8].set_config(msg.payload)

def process_command(id, msg): # TODO: CHANGE THIS TO USE MSG.ID FOR PROD.

    to_command = id - BASE_ID - 4

    i = j = 0
    while i < 8:
        channel[to_command + j].set_command(msg[i:i+2])
        i += 2
        j += 1


# MAIN LOOP HERE

# feedback_tick = time.monotonic_ns() * 1E-6

# while True:
#     elapsed_time = time.monotonic_ns() * 1E-6 - feedback_tick
#     if elapsed_time >= 100:
#         print(elapsed_time)
#         send_feedback()
#         feedback_tick = time.monotonic_ns() * 1E-6

# READ AND PROCESS CANBUS MESSAGES HERE
