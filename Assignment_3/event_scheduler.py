#! /usr/bin/env python3

import sched
import time, datetime
import threading
from twilio.rest import TwilioRestClient
import RPi.GPIO as GPIO

# Set pin mode to the numbers you can read off the pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up channel list
chan_list = [13, 19, 26]  # 13 red, 19 green, 26 blue
GPIO.setup(chan_list, GPIO.OUT)


def sendText(body):
    twilioClient = TwilioRestClient(accountSID, authToken)
    twilioNumber = '+12403033631'
    myNumber = 'myCellNumber'

    message = twilioClient.messages.create(body=body, from_=twilioNumber, to=myNumber)


def beep():
    print("Not implemented")


def flashLED():
    while True:
        GPIO.output(chan_list, (True, True, True))
        sleep(1)
        GPIO.output(chan_list, (False, False, False))
        sleep(1)


def start_alerts():
    threading.Thread(target=sendText).start()
    threading.Thread(target=beep).start()
    threading.Thread(target=flashLED).start()


def exit_led():
    GPIO.output(chan_list, (False, False, False))
    threading._Thread_stop()


def end_alerts():
    t = threading.Timer(900, exit_led)
    t.start()


def event_scheduler(events):
    s = sched.scheduler(time.time, time.sleep)
    for event in events:
        s.enterabs(time=event.start, action=start_alerts)
        end_time = event.start + datetime.timedelta(minutes=15)
        s.enterabs(time=end_time, action=end_alerts)
    GPIO.cleanup(chan_list)
