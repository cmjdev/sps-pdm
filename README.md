# What is it?
SPS-PDM is an open source project meant to produce a cheap and reliable Canbus Power Distribution module.  

The goal of this project is to provide a base for others to extend and make their own but should work as is with no modifications according to the default specifications

# Specifications
- Feedback messages are sent at 20Hz
- Command messages are expected at 50Hz
- Fusing and shutdown logic to be performed at minimum 100Hz


# Design Choices
## Software
Python was chosen as the language for this project due to it's simplicity and readability.  The base specifications for the SPS-PDM are easily achieved using **CircuitPython** and pre-existing libraries.
This project is meant to be ported, extended, and used for many more complicated scenarios and choosing Python provides a sort of pseudo-code / boiler plate to get started with your langauge/platform of choice.

## Hardware
Currently this project is designed/tested using the **Adafruit RP2040 CAN Bus Feather**.  The reason for choosing this platform was soley based on the packaging.  It is a device with can controller/tranceiver on board and has 6MB of useable storage space after firmware to do some logging.  **This is not an automotive grade solution and should be treated as such.**