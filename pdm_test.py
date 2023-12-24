import json
import asyncio
import sys
from channel import Channel

if sys.implementation.name == "circuitpython":
    import board
    import busio
    from digitalio import DigitalInOut
    from adafruit_mcp2515.canio import Message
    from adafruit_mcp2515 import MCP2515 as CAN

    cs = DigitalInOut(board.CAN_CS)
    cs.switch_to_output()
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    can_bus = CAN(spi, cs)

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


def process_config(id, msg):
    to_command = id - BASE_ID - 8

    channel[to_command].set_config(msg)

def process_command(id, msg):
    # TODO: Add reset functionality into command message
    to_command = id - BASE_ID - 4

    j = 0
    for i in range(0, 8, 2):
        channel[to_command + j].set_command(msg[i : i + 2])
        j += 1

async def send_feedback():
    while True:
        
        base = BASE_ID
        shutdown = False
        current = 0

        for i, c in enumerate(channel):
            ch = i % 4

            # TODO: Send battery voltage

            # set current
            message[ch] = int(c.current / 50)
            current += c.current

            # set shutdown
            set_mask(ch, c.shutdown, SHUTDOWN_OFFSET, SHUTDOWN_MASK)
            shutdown = c.shutdown or shutdown

            # set status
            set_mask(ch, c.status, STATUS_OFFSET, STATUS_MASK)

            # set active
            set_mask(ch, c.active, ACTIVE_OFFSET, ACTIVE_MASK)



            if ch == 3:
                message[7] = message[7] or shutdown
                message[6] = min(int(current/100), 255)

                if sys.implementation.name == "circuitpython":
                    msg = Message(BASE_ID, message)
                    can_bus.send(msg)
                else:
                    pass
                base = base + 1
        await asyncio.sleep_ms(43)


async def listenerz():
    while True:
        with can_bus.listen() as listener:
            message_count = listener.in_waiting()
            for i in range(message_count):
                msg = listener.receive()

                # TODO: Make ids an offset from base for flexibility
                if msg.id < 0x66E:
                    process_command(msg.id, msg.data)
                elif msg.id < 0x67E:
                    process_config(msg.id, msg.data)
        await asyncio.sleep_ms(20)


async def main():
    tasks = []
    tasks.append(asyncio.create_task(send_feedback()))
    tasks.append(asyncio.create_task(listenerz()))
    for ch in channel:
        tasks.append(asyncio.create_task(ch.process()))
    await asyncio.gather(*tasks)


# Create all channels according to config
channel = [Channel(**c) for c in config]

if sys.implementation.name == "circuitpython":
    asyncio.run(main())
