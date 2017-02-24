#! /usr/bin/env python3

import RPi.GPIO as GPIO
import time

#set pin mode to the numbers you can read off the pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set up channel list
chan_list = [13,19,26] #13 red, 19 green, 26 blue
GPIO.setup(chan_list, GPIO.OUT)

#modify these to be from data
input = 0.2

#Display LED based on threshold and input
if input < .25:
        GPIO.output(chan_list, (False,True,False)) #green
elif input < .5:
        GPIO.output(chan_list, (True,True,False)) #yellow
else:
        GPIO.output(chan_list, (True,False,False)) #red


time.sleep(2)
GPIO.cleanup(chan_list)