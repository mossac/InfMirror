#!/usr/bin/python3
from time import sleep
import math
import Adafruit_BBIO.GPIO as GPIO
import time



 

length = 35
max = 32
sw4 = "P9_42"
GPIO.setup(sw4, GPIO.IN)
# Open a file
fo = open("/dev/rpmsg_pru30", "wb", 0)


def redbut(channel):
        print("triggered")
        for i in range(0, length):
                fo.write(b"%d %d %d %d %d\n" % (i, 0, 50, 0, 0))
                    # print("0 0 127 %d" % (i))
                fo.write(b"-1 0 0 0 0\n");    # Send colors to LEDs
        
        for i in range(0, length):
            fo.write(b"%d %d %d %d %d\n" % (i, 0, 0, 50, 20))
            # print("0 0 127 %d" % (i))
            fo.write(b"-1 0 0 0 0\n");    # Send colors to LEDs
            
        
            
GPIO.add_event_detect(sw4, GPIO.RISING, callback=redbut, bouncetime=500)

while True:
    time.sleep(0)
            
# Close opened file
fo.close()