#! /usr/bin/env python3

import sched
import time
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


def start_alerts():
    stop_event = threading.Event()

    threading.Thread(target=beep, kwargs={"stop_event": stop_event}).start()
    threading.Thread(target=flashLED, kwargs={"stop_event": stop_event}).start()

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
        # schedule the sms alert
        s.enterabs(time=event['start'], action=sendText, argument=[accountSID, authToken, myNumber, event], priority=1)
        # schedule the led/audio alerts
        s.enterabs(time=event['start'], action=start_alerts, priority=1)
    s.run(blocking=True)

    GPIO.cleanup(chan_list)
