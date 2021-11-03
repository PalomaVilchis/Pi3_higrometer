#!/usr/bin/python3
 
import spidev
import time
 
def readChannel(spi, analog_channel):
    """
    Reads an analog channel through a SPI device. The function builds a 3-byte 
    frame formatted as 00000001-1,D2,D1,D0,0000-00000000. The one of the first
    byte corresponds to the start bit that initializes the SPI communication 
    between the master and the slave. Bits 1, D2, D1 and D0 of the second byte 
    corresponds to the control bits needed to request a reading from the ADC 
    (check the MCP3008 datasheet, Fig. 5-1). The following trailing zeros of 
    the third byte do not care.
    Note:
    The spi.xfer() method sends a three-element list containg the 
    aforementioned frame to the ADC. The method returns a 10-bit reading in a 
    three-element little-endian list (the least significant byte is stored in 
    reading[2]).
    Arguments:
        spi: An SPI object created with spidev.SpiDev()
        analog_channel: An integer between 0 and 7
    Returns:
        A digital reading that ranges from 0 to 1023
    """
    comm_mode = 1
    ctrl_bits = (comm_mode << 3) + analog_channel
    frame = [1, ctrl_bits << 4, 0]
    reading = spi.xfer(frame)
    return int((reading[1] << 8) + reading[2])

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
                print('No reading...')
            time.sleep(delay)
            timestamp += delay
    except KeyboardInterrupt:
        print("\nCancel")

if __name__ == "__main__":
    main()