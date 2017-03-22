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


def beep(stop_event):
    while not stop_event.is_set():
        print("Not implemented")

    # exit/cleanup


def flashLED(stop_event):
    while not stop_event.is_set():
        GPIO.output(chan_list, (True, True, True))
        time.sleep(1)
        GPIO.output(chan_list, (False, False, False))
        time.sleep(1)
    # exit
    GPIO.output(chan_list, (False, False, False))


def start_alerts():
    stop_event = threading.Event()

    threading.Thread(target=sendText).start()
    threading.Thread(target=beep, args=stop_event).start()
    threading.Thread(target=flashLED, args=stop_event).start()

    time.sleep(900)

    stop_event.set()


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
