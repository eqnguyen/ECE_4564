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


def beep():
    t = threading.Timer(900, exit_beep)
    t.start()
    print("Not implemented")


def flashLED():
    t = threading.Timer(900, exit_led)
    t.start()
    while True:
        GPIO.output(chan_list, (True, True, True))
        time.sleep(1)
        GPIO.output(chan_list, (False, False, False))
        time.sleep(1)


def start_alerts():
    threading.Thread(target=sendText).start()
    threading.Thread(target=beep).start()
    threading.Thread(target=flashLED).start()


def exit_led():
    GPIO.output(chan_list, (False, False, False))
    threading._Thread_stop()


def exit_beep():
    threading._Thread_stop()


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
