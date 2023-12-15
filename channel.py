import asyncio

class Channel:
    def __init__(
        self,
        fuse_min,
        fuse_max,
        fuse_inrush,
        fuse_delay,
        soft_start,
        retry_delay,
        pwm_mode,
    ):
        # Feedback
        self.current = 0
        self.shutdown = False
        self.status = 0
        self.active = False

        # Command
        self.duty = 0
        self.freq = 0

        # Config
        self.fuse_min = fuse_min
        self.fuse_max = fuse_max
        self.fuse_inrush = fuse_inrush
        self.fuse_delay = fuse_delay
        self.soft_start = soft_start
        self.retry_delay = retry_delay
        self.pwm_mode = pwm_mode

    async def intake(self):
        while True:
            print("Getting current")
            await asyncio.sleep(1)

    async def process(self):
        while True:
            print("Processing Channel")
            await asyncio.sleep(1)

    def set_command(self, msg): # takes byte with combined duty/frequency/reset
        # set duty / freq
        self.duty = min(msg[0], 100)
        self.freq = min(msg[1] * 2, 500)

    def set_config(self, msg): # takes and converts the raw canbus message
        # parse and set config variables
        self.fuse_min = msg[0] * 10  # 255 * 10 -> 2550 -> 25.5A
        self.fuse_max = msg[1] * 10  # 255 * 10 -> 2550 -> 25.5A
        self.fuse_inrush = msg[2] * 30  # 255 * 30 -> 7650 -> 76.5A
        self.fuse_delay = msg[3] * 20  # 255 * 20 -> 5100ms
        self.soft_start = msg[4] * 20  # 255 * 20 -> 5100ms
        self.retry_delay = msg[5] * 20  # 255 * 20 -> 5100ms
        self.pwm_mode = (msg[6] & 192) >> 6  # 192 is mask for pwm_mode
