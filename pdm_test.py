import json

with open("config.json") as f:
    config = json.load(f)

message = bytearray(8)
channel = []

# ci Stores the byte index, offsets and masks for channel feedback
# Byte Index(0), Shutdown Offset(1), Shutdown Mask(2), Status Offset(3), Status Mask(4), Active Offset(5), Status Offset(6)
ci = [(4,7,128,5,96,4,16), (4,3,1,1,6,0,1), (5,7,128,5,96,4,16), (5,3,1,1,6,0,1)]

BASE = 0x666

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

class Channel:
    def __init__(self):

        # Feedback
        self.current = 0
        self.shutdown = False
        self.status = 0
        self.active = False

        # Command
        self.duty = 0
        self.freq = 0

        # Config
        self.fuse_min = 0
        self.fuse_max = 0
        self.fuse_inrush = 0
        self.fuse_delay = 0
        self.soft_start = 0
        self.pwm_mode = 0

def set_mask(channel, value, offset, mask):
    if channel % 2: # Even Channels
        message[ci[channel][0]] = message[ci[channel][0]] & ~ci[channel][mask]
        message[ci[channel][0]] = message[ci[channel][0]] | value << ci[channel][offset] 
    else: # Odd Channels
        message[ci[channel][0]] = message[ci[channel][0]] & ~ci[channel][mask]
        message[ci[channel][0]] = message[ci[channel][0]] | value << ci[channel][offset]

def send_feedback():

    base = BASE
    for i,c in enumerate(channel):

        ch = i % 4
        
        # set current
        message[ch] = c.current
        
        # set shutdown
        set_mask(ch, c.shutdown, SHUTDOWN_OFFSET, SHUTDOWN_MASK)

        # set s1tatus
        set_mask(ch, c.status, STATUS_OFFSET, STATUS_MASK)

        # set active
        set_mask(ch, c.active, ACTIVE_OFFSET, ACTIVE_MASK)

        if ch == 3:
            print(hex(base), message)
            base = base + 1

for i in range(4):

    # TODO: FIGURE OUT NICER WAY TO DO THIS
    # MAYBE SOMETHING BASED ON KEY NAMES / MAPS?
    channel.append(Channel())
    channel[i].fuse_min = config[i]['fuse_min']
    channel[i].fuse_max = config[i]['fuse_max']
    channel[i].fuse_inrush = config[i]['fuse_inrush']
    channel[i].fuse_delay = config[i]['fuse_delay']
    channel[i].soft_start = config[i]['soft_start']
    channel[i].pwm_mode = config[i]['pwm_mode']


# SET UP FEEDBACK MESSAGE 20Hz?

# MAIN LOOP HERE

