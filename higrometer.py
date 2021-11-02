#!/usr/bin/python3
 
import spidev
import os
import time
 
def readChannel(spi, analog_channel):
    val = spi.xfer2([1, (8 + analog_channel) << 4, 0])
    data = ((val[1] & 3) << 8) + val[2]
    return data

def main():
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000
    delay = 5.0
    timestamp = 0.0
    analog_channel = 7
    print("Starting...")
    try:
        while True:
            val = readChannel(spi, analog_channel)
            if val != 0:
                print('Reading: {} at time {} s'.format(val, timestamp))
            else:
                print("No reading...")
            time.sleep(delay)
            timestamp += delay
    except KeyboardInterrupt:
        print("Cancel")

if __name__ == "__main__":
    main()
