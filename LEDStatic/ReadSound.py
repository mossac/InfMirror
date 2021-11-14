#!/usr/bin/python3
#//////////////////////////////////////
#	blink.py
#	Blinks one LED wired to P9_14.
#	Wiring:	P9_14 connects to the plus lead of an LED.  The negative lead of the
#			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
#			to ground.
#	Setup:	
#	See:	
#//////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time

sw4 = "P9_42"
GPIO.setup(sw4, GPIO.IN)
def redbut(channel):
    state = GPIO.input(channel)
    print("trigger")
        
            
GPIO.add_event_detect(sw4, GPIO.RISING, callback=redbut, bouncetime=100)
 

 
while True:
  
    time.sleep(0.01)
    
    state = GPIO.input(sw4)
    print(state )