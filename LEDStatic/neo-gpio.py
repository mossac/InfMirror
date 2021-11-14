#!/usr/bin/python3
from time import sleep
import math
import Adafruit_BBIO.GPIO as GPIO
import time
import Adafruit_BBIO.ADC as ADC


 
global flag
flag = 0
length = 35
max = 32
sw4 = "P9_42"
GPIO.setup(sw4, GPIO.IN)
ADC.setup()
# Open a file
fo = open("/dev/rpmsg_pru30", "wb", 0)

colors = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[1,0,1,0]]# colors = [[1,0,0],[1,0,0]]

oldr=0
oldb=0
oldg=0
oldw=0
         

def setred(channel):
    #print("FLAGSET HIGH")
    global flag
    flag = 1
    for i in range(0, length):
        fo.write(b"%d %d %d %d %d\n" % (i, 50, 0, 0, 0))
                    # print("0 0 127 %d" % (i))
                    # Send colors to LEDs
    fo.write(b"-1 0 0 0 0\n");
    sleep(.07)
    #print("FLAGSET LOW")
    flag = 0

GPIO.add_event_detect(sw4, GPIO.RISING, callback=setred, bouncetime=30)

while True:
    for color in colors:
        newr = color[0]
        newg = color[1]
        newb = color[2]
        neww = color[3]
        maxtime=20
        for time in range(0, maxtime):
            r = (max*oldr+(newr-oldr)*max*time/maxtime)
            g = (max*oldg+(newg-oldg)*max*time/maxtime)
            b = (max*oldb+(newb-oldb)*max*time/maxtime)
            w = (max*oldw+(neww-oldw)*max*time/maxtime);
            for i in range(0, length):
                if (flag == 0): 
                    fo.write(b"%d %d %d %d %d\n" % (i, r, g, b, w))
                # print("0 0 127 %d" % (i))
               
            fo.write(b"-1 0 0 0 0\n");    # Send colors to LEDs
            
            # print (r,g,b)
            
            sleep(0.05)
            
        oldr=newr
        oldg=newg
        oldb=newb
        oldw = neww
        
        #print(flag)
        #if (flag == 1):
         #   for i in range(0, length):
          #          fo.write(b"%d %d %d %d %d\n" % (i, 50, 0, 0, 0))
           #         # print("0 0 127 %d" % (i))
            #        # Send colors to LEDs
            ##fo.write(b"-1 0 0 0 0\n");
            #sleep(1)
            #flag = 0
        
# Close opened file
fo.close()