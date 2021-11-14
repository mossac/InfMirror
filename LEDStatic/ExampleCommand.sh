#!/bin/bash
echo 0 0 0 0 127 > /dev/rpmsg_pru30 
#USAGE: echo "Led position, R,G,B,W" 
#Previous line makes led at postion 0 white
echo -1 > /dev/rpmsg_pru30
#send the command