# Raspberry Pi soil moisture monitor

This document explains how to measure the soil level moisture by means of an cheaper sensor connected to a Raspberry Pi 3. Other Pi versions should support this project, also. 

An soil moisture sensor is made up by two pieces: a sensing probes and an electronic module emitting both an analogic signal and a digital signal. The sensing probes are two nickel-coated copper tracks separated by 0.25", namely T1 and T2. The electronic module consists of an operational amplifier comparator that produces the digital output. 

The analogic output is directly produced by the probes when T2 receives the electrical current that passes through the soil when T1 is connected to a 3.3 V power supply.

The soil acts as a bridge connecting the tracks. The electrical current passing through the bridge is proportional to the soil moisture level so that the higher the moisture level, the higher the current that T2 receives. In this way, the sensor produces an analogic signal that ranges from 0 V to 3.3 V. The first voltage value is expected when the soil is too moist, meanwhile the second value is expected when the soil is too dry

The Raspberry PI cannot processed analogic signals, as the one the moisture sensor produces, by itself. An analog-digital converter (ADC) is needed to convert the analog signal to a digital one. The MCP 3008 ADC acts as an interface between the sensor and the Raspberry Pi. It receives an analog signal that is converted to a digital level ranging from 0 to 1023. In this way, 0 V produces a digital value of zero and 3.3 V produces a digital value of 1023.

The SPI protocol is used to establish the communication rules between the Raspberry Pi 3 and the moisture sensor. The output code that the ADC sends to the Raspberry Pi is equal to

$\frac{1024(V_{IN})}{V_{REF}}$,

where $V_{IN}$ corresponds to 3.3 V for this application and $V_{REF}$ corresponds to the amplitude of the analog signal that the moisture sensor produces.

A Python script processes the digital output code that the ADC produces. This script reads each *delay* seconds the code the ADC emits. The user can read de moisture level in the standard output. The script execution finishes when typing `ctrl + c`.

## Components

### Hardware

1. A Raspberry Pi.
2. A soil moisture sensor (a.k.a. higrometer).
3. A pair female-female dupont cables.
4. A MCP3008 analog-digital converter.
5. A GPIO Cobbler Plus V2 or similar.
6. A protoboard.
7. Protoboard wires.

### Software

1. ssh.
2. Python v3.0+ interpreter.
   1. pip3 software manager.
   2. spidev library.

## Connections

Moisture sensor  | MCP3008       | Raspberry
---------------  | ------------- | -------------
VCC              | VDD           | 3V3
AO               | CH7           | --
GND              | DGND          | GND
--               | AGND          | GND
--               | CLK           | SCLK
--               | DOUT          | MISO
--               | DIN           | MOSI
--               | CS/SHDN       | CE0

## Python script

```Python
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
```

## Script execution

On a command terminal, follow these instructions:

1. Connect to the Raspberry with ssh: `ssh user@pi`.
2. Install the spidev library with pip: `pip3 install spidev`.
3. Create a folder to hold this project: `mkdir moisture`.
4. Change directory: `cd moisture`.
5. Clone the project: `git clone https://github.com/Ryuuba/Pi3_higrometer.git .`
6. Run the script in privilage mode: `sudo .\moisture.py`

The success of the above mentioned instructions requires that the SPI dev of the Raspberry Pi is properly enable. On Ubuntu Server, this is accomplished following these instructions:

```Bash
sudo groupadd spiuser
sudo usermod -aG spiuser your_user
sudo chown :spiuser /dev/spidev0.0
sudo chmod g+rw /dev/spidev0.0
```

## Bibliography

1. https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf
2. https://tutorials-raspberrypi.com/measuring-soil-moisture-with-raspberry-pi/
3. https://askubuntu.com/questions/1273700/enable-spi-and-i2c-on-ubuntu-20-04-raspberry-pi