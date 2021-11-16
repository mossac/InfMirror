#!/usr/bin/python3
from time import sleep
import math
import Adafruit_BBIO.GPIO as GPIO
import time
import Adafruit_BBIO.ADC as ADC


 
global flag
flag = 0
length = 18
max = 32
sw4 = "P9_42"
GPIO.setup(sw4, GPIO.IN)
ADC.setup()
# Open a file
fo = open("/dev/rpmsg_pru30", "wb", 0)

colors = [[1,0,0,0],[1,1,0,0]]# colors = [[1,0,0],[1,0,0]]

oldr=0
oldb=0
oldg=0
oldw=0
         

def setred(channel):
    #print("FLAGSET HIGH")
    global flag
    
    #print("FLAGSET LOW")
    flag = ~flag
    sleep(.1)

GPIO.add_event_detect(sw4, GPIO.RISING, callback=setred, bouncetime=450)

while True:
    if(flag == 0):
        for i in range(0, length):
            if(i < math.floor(length/2)-2):
                fo.write(b"%d %d %d %d %d\n" % (i, 0, 0, 0, 50))
                    # print("0 0 127 %d" % (i))
                    # Send colors to LEDs
            elif ((i <= math.floor(length/2)+1) and (i >= math.floor(length/2)-2) ):
                fo.write(b"%d %d %d %d %d\n" % (i, 50, 0, 50, 0))
            elif (i > (length/2)):
                fo.write(b"%d %d %d %d %d\n" % (i, 0, 0, 50, 0))
        fo.write(b"-1 0 0 0 0\n");
        sleep(.07)
    else:
        for i in range(0, length):
            if(i > 10.5):
                fo.write(b"%d %d %d %d %d\n" % (i, 0, 0, 0, 50))
                    # print("0 0 127 %d" % (i))
                    # Send colors to LEDs
            elif (i <= 10 and i >= 7 ):
                fo.write(b"%d %d %d %d %d\n" % (i, 50, 0, 50, 0))
            elif (i < 7):
                fo.write(b"%d %d %d %d %d\n" % (i, 0, 0, 50, 0))
        fo.write(b"-1 0 0 0 0\n");
        sleep(.07)
fo.close()