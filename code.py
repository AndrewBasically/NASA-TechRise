import adafruit_sdcard
import bitbangio
import board
import busio
import digitalio
import os
import random
import storage
import time

# Connect to the card and mount the filesystem.
spi = bitbangio.SPI(board.CLK, board.CMD, board.DAT0)
cs = digitalio.DigitalInOut(board.DAT3)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Define array size
ARRAY_SIZE = 10000

# Create zero array
ZERO_ARRAY = [0] * ARRAY_SIZE

# Create one array
ONE_ARRAY = [1] * ARRAY_SIZE

# Get start time
start_time = time.monotonic()

#Order of information
with open("/sd/SDlog.txt", "a") as f:
        f.write("Time, Array, Count\n")

while True:
    # Get current time
    current_time = int(time.monotonic() - start_time)

    # Test for bit flip
    if sum(ZERO_ARRAY) > 0:
        # Open file for append
        with open("/sd/SDlog.txt", "a") as f:
            f.write("{}, 0, {}\n".format(current_time, sum(ZERO_ARRAY)))
        print("Time:", current_time, "-", "Message: Bit flip detected in ZERO_ARRAY! Count:", sum(ZERO_ARRAY))
        ZERO_ARRAY = [0] * ARRAY_SIZE

    if sum(ONE_ARRAY) < len(ONE_ARRAY):
        # Open file for append
        with open("/sd/SDlog.txt", "a") as f:
            f.write("{}, 1, {}\n".format(current_time, len(ONE_ARRAY) - sum(ONE_ARRAY)))
        print("Time:", current_time, "-", "Message: Bit flip detected in ONE_ARRAY! Count:", len(ONE_ARRAY) - sum(ONE_ARRAY))
        ONE_ARRAY = [1] * ARRAY_SIZE

    # Wait for 10 seconds
    time.sleep(10)
