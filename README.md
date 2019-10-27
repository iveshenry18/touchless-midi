# Touchless MIDI
Scripts for running a distance sensor as a MIDI Continuous Controller on a Raspberry Pi

**Disclaimer: the code in this repo was written for a University project and as such is not designed for portability**

This repo consists of a couple of a Bash script, a couple Python scripts, and a Pure Data patch for running a distance sensor as a MIDI controller on a Raspberry Pi, which can communicate over a network via RTP MIDI with another machine.

## Required Software
The required software includes but may not be limited to:
- PIGPIO
- ALSA
- aconnectgui
- [raveloxmidi](https://github.com/ravelox/pimidi/)
- wmctrl
- Pure Data

## Required Hardware
This project was designed to run on a Raspberry Pi 4 Model B and an HC-SR05 distance sensor module.
The circuit used is very similar to what is described [here](https://pimylifeup.com/raspberry-pi-distance-sensor/) and [here](https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/) (huge thanks to these creators for their tutorials).

## Files

### distance_sensor.py
An object-oriented adaptation of the scripts provided by the aforementioned tutorials. This assumes the TRIGGER is wired to GPIO pin 4, and the ECHO is wired to GPIO pin 27 (BCM), but can be fairly easily adjusted to suit other wiring options.

### control_MIDI.py
Defines a class MIDI_Distance_Controller which utilizes a Distance_Sensor object and translates distance data to MIDI values, sending these over a socket to be received by receiver.pd. This takes an optional command-line argument to set which Continuous Controller it sends to.

### receiver.pd
A simple Pure Data patch which handles the values sent over socket from control_MIDI.py and routes them to ctlout. Also can handle MIDI in and the input of another controller, simply passing these to noteout and ctlout.

### raveloxmidi.conf
Configuration file for raveloxmidi. Must adjust network.bind_address to IP of your Pi. **Must be symlinked to `/etc/raveloxmidi.conf`**

### control_midi
A master Bash script to run all programs in a single command. Launches the receiver.pd in the background as well as ALSA gui, then creates the necessary midi connections (from the output of receiver.pd to the first available Virtual Raw MIDI channel, as well as from an option Digital Piano to the input to receiver.pd). It then launches raveloxmidi with the configuration file (temporarily modified to handle possible variations in the Virtual Raw MIDI channel), and finally runs the control_MIDI.py. This script can be run with one positional argument for the Continuous Controller number. If no argument is given, it defaults to 11. After the python script is stopped by the user, the other processes are killed. **To be symlinked to `~/bin/control_midi`**

**Note: this uses absolute paths, designed such that this repository is under ~/Documents/TouchlessMIDI**

## Thanks
This project wouldn't have been possible without the help of countless resources and similar open-source projects. Specific shoutouts go to [Dave Kelly](https://www.raveloxprojects.com/blog/?p=496) and [Pi My Life Up](https://pimylifeup.com/raspberry-pi-distance-sensor/) for the resources they provided.
