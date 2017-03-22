#! /usr/bin/env python3

import sched
import time
import threading
from twilio.rest import TwilioRestClient
import RPi.GPIO as GPIO

chan_list = []


def sendText(accountSID, authToken, body):
    twilioClient = TwilioRestClient(accountSID, authToken)
    twilioNumber = '+12403033631'
    myNumber = 'myCellNumber'

    message = twilioClient.messages.create(body=body, from_=twilioNumber, to=myNumber)


def beep(run_flag):
    while run_flag:
        print("Not implemented")

    # exit/cleanup


def flashLED(run_flag):
    while run_flag:
        GPIO.output(chan_list, (True, True, True))
        time.sleep(1)
        GPIO.output(chan_list, (False, False, False))
        time.sleep(1)
    # exit
    GPIO.output(chan_list, (False, False, False))


def start_alerts():
    run_flag = True

    threading.Thread(target=sendText).start()
    threading.Thread(target=beep, args=run_flag).start()
    threading.Thread(target=flashLED, args=run_flag).start()

    time.sleep(900)

    run_flag = False


def event_scheduler(events):
    # Set pin mode to the numbers you can read off the pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set up channel list
    chan_list = [13, 19, 26]  # 13 red, 19 green, 26 blue
    GPIO.setup(chan_list, GPIO.OUT)

    s = sched.scheduler(time.time, time.sleep)
    for event in events:
        s.enterabs(time=event.start, action=start_alerts)
    s.run(blocking=True)

    GPIO.cleanup(chan_list)
