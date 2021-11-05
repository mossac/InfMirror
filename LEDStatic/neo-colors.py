#!/usr/bin/python3
from time import sleep
import math

length = 61
max = 24

# Open a file
fo = open("/dev/rpmsg_pru30", "wb", 0)

colors = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[1,0,1,0]]# colors = [[1,0,0],[1,0,0]]

oldr=0
oldb=0
oldg=0
oldw=0

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
                fo.write(b"%d %d %d %d %d\n" % (i, r, g, b, w))
                # print("0 0 127 %d" % (i))
            fo.write(b"-1 0 0 0 0\n");    # Send colors to LEDs
            
            # print (r,g,b)
            
            sleep(0.05)
            
        oldr=newr
        oldg=newg
        oldb=newb
        oldw = neww
# Close opened file
fo.close()