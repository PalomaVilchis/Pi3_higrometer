# Raspberry Pi soil moisture monitor

In this document explains how to measure the soil level moisture by means of an cheaper sensor connected to a Raspberry Pi 3. Other Pi versions should support this project, also. 

An  soil moisture sensor is made up by two pieces: a sensing probes and an electronic module emitting both an analogic signal and a digital signal. The sensing probes are two nickel-coated copper tracks separated by 0.25", namely T1 and T2. The electronic module consists of an operational amplifier comparator that produces the digital output. 

The analogic output is directly produced by the probes when T2 receives the electrical current that passes through the soil when T1 is connected to a 3.3 V power supply.

The soil acts as a bridge connecting the tracks. The current passing through the bridge is proportional to the soil moisture level so that the higher the moisture level, the higher the current that T2 receives. In this way, the sensor produces an analogic signal that ranges from 0 V to 3.3 V. The first voltage value is expected when the soil is too dry, meanwhile the second value is expected when the soil is too moist.

The Raspberry PI cannot processed analogic signals, as the one the moisture sensor produces. An analog-digital converter (ADC) is needed to convert the analog signal to a digital one. The MCP 3008 ADC acts as an interface between the sensor and the Raspberry Pi. It receives an analog signal that is converted to a digital level ranging from 0 to 1023. In this way, 0 V produces a digital value of zero and 3.3 V produces a digital value of 1023.

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

1. git.
2. ssh.
3. VS Code with extensions:
   1. Python.
   2. Remote-SSH.
4. Python v3.0+ interpreter.
   1. pip3 software manager.
   2. spidev library.

## Circuit

## Python script

