import asyncio
import sys

if sys.implementation.name == "circuitpython":
    import microcontroller
    import analogio
    import digitalio
    import board

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
        input_pin,
        output_pin,
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
        self.input_pin = getattr(board, input_pin)
        self.output_pin = getattr(board, output_pin)

        if sys.implementation.name == "circuitpython":
            self.input_pin = analogio.AnalogIn(self.input_pin)
            self.output_pin = digitalio.DigitalInOut(self.output_pin)
            self.output_pin.direction = digitalio.Direction.OUTPUT

    async def process(self):
        while True:
            if sys.implementation.name == "circuitpython":
                self.current = self.input_pin.value
                
                if self.current < 100: self.output_pin.value = True
                else: self.output_pin.value = False

                print(self.current)
            else: print("Process Inputs Here")
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
