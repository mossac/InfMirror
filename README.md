# ECE434 - Final Project: Infinity Mirror

**Aidan Moss & Tyler Thenell**



### Project Overview

For our project, we decided to make a music/audio responsive infinity mirror. This project will serve as a home decoration for audio visualization. 



### Parts

The Infinity Mirror uses the following parts:

- [ ] Acrylic Sheets (~$75)
- [ ] SK6812 LEDs (~$55)
- [ ] One way mirror window film (~$24)
- [ ] BeagleBone Black (~$53)
- [ ] KY-037 (~$8)
- [ ] Wire



### Tools

The Infinity mirror needed the following tools to assemble:

- [ ] Jigsaw
- [ ] Soldering Iron
- [ ] Exacto Knife
- [ ] Hot glue gun
- [ ] Tape



### Pinouts

Physical Pinout:

·P9_29 → LED Strip data line

·P9_40 → Microphone Digital Output



### Hardware

This image shows how the data lines of the LEDs were connected. Segment 0 represents the first segment in the datapath. Each colored segment array in the diagram is connected in parallel. Each segment is 7 leds long. This means you have a total length of 35 LEDs due to the parallelism. If you turn LED 3 on, the third LED will turn on in Green, Yellow, Grey, Blue, and Orange.

![alt text](https://github.com/mossac/InfMirror/blob/master/LED-Schematic.png?raw=true)

This image shows how the BeagleBone Black is connected to the audio sensor and LED strip. Based on the diagram above, the LED segment below is really 5 parallel LED strips. 

![alt text](https://github.com/theneltj/Embedded-Linux/blob/master/hw09/TempLog.png?raw=true)

### Installation

Clone repo located here:  https://github.com/mossac/InfMirror

This repo contains all the code needed to run the SK6812 LED strands to begin running the PRU driver simply:

```shell
$ cd InfMirror/LEDStatic
$ source setup.sh
$ make
```

The kernel driver should be active, to test you can run commands in ExampleCommand.sh which will turn the first LED in your strip white if it is running correctly if not follow the commands in **section 1.16 of the link below** as you may not have the rpmsg.pru driver installed that the kernel driver requires:

https://markayoder.github.io/PRUCookbook/05blocks/blocks.html



### Controlling LEDs

After running the PRU kernel driver, you can begin programming or running our example LED control code. 

To run any of the sample python programs from the repo simply use the command

`$ ./filename.py`

Listed below is a quick rundown of what you can expect from the different sample programs

- [neo-colors.py](http://neo-colors.py/): Shifts the LEDs slowly through 4 different vibrant colors
- [neo-rainbow.py](http://neo-rainbow.py/): Runs all the colors of the rainbow through the each induvial LED quickly
- [neo-gpio.py](http://neo-gpio.py/): Same as [neo-colors.py](http://neo-colors.py/) but has integrated a microphone input that flashes the LEDs red when a adequate input is detected
- [neo-gpioFlip.py](http://neo-gpioflip.py/): Top half of the hardware is white middle strip is purple and bottom few are blue flips when a adequate microphone input is detected
- [simplemic.py](http://simplemic.py/): Testing program we used, checks from microphone input of certain level and flashes two colors if found

We recommend checking out these files and reading the section below, we tried to make them easy to understand and hope that others can build on them to create even more unique shows.







