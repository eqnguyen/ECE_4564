#! /usr/bin/env python3

import sched
import time, datetime
import threading
from twilio.rest import TwilioRestClient
import pygame
import RPi.GPIO as GPIO

chan_list = []


def sendText(accountSID, authToken, myNumber, event):
    twilioClient = TwilioRestClient(accountSID, authToken)
    twilioNumber = '+12403033631'
    body = 'Test'
    message = twilioClient.messages.create(body=body, from_=twilioNumber, to=myNumber)


def beep(stop_event):
    while not stop_event.is_set():
        pygame.mixer.init()
        pygame.mixer.music.load('notification.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue


def flashLED(stop_event):
    while not stop_event.is_set():
        GPIO.output(chan_list, (True, True, True))
        time.sleep(1)
        GPIO.output(chan_list, (False, False, False))
        time.sleep(1)
    # exit
    GPIO.output(chan_list, (False, False, False))


def start_alerts(start_time):
    stop_event = threading.Event()

    threading.Thread(target=beep, kwargs={"stop_event": stop_event}).start()
    threading.Thread(target=flashLED, kwargs={"stop_event": stop_event}).start()

    # if the alerts were started after 15min before the event, adjust the time to sleep
    if start_time < time.time():
        # sleep for 900sec minus the time that has already elapsed
        adjusted_sleep = 900 - (time.time() - start_time)
        # make sure adjusted_sleep is positive
        adjusted_sleep = adjusted_sleep if (adjusted_sleep > 0) else 0
        time.sleep(adjusted_sleep)
    else:
        # sleep for 15min or 900sec
        time.sleep(900)

    stop_event.set()


def event_scheduler(accountSID, authToken, myNumber, events):
    # Set pin mode to the numbers you can read off the pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set up channel list
    global chan_list
    chan_list = [13, 19, 26]  # 13 red, 19 green, 26 blue
    GPIO.setup(chan_list, GPIO.OUT)

    s = sched.scheduler(time.time, time.sleep)
    for event in events:
        # the alerts are scheduled 15min before the event
        start_time = event['start'] - datetime.datetime.timedelta(900)
        # sched needs a value of type double
        start_time = time.mktime(start_time.timetuple())

        # schedule the sms alert
        s.enterabs(time=start_time, action=sendText, argument=[accountSID, authToken, myNumber, event], priority=1)
        # schedule the led/audio alerts
        s.enterabs(time=event['start'], action=start_alerts, priority=1)
    s.run(blocking=True)

    GPIO.cleanup(chan_list)
