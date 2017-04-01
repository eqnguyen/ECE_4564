#! /usr/bin/env python3

import datetime
import sched
import threading
import time

import RPi.GPIO as GPIO
import pygame
from twilio.rest import TwilioRestClient

chan_list = []


def send_text(account_sid, auth_token, my_number, event_start):
    twilio_client = TwilioRestClient(account_sid, auth_token)
    twilio_number = '+12403033631'
    date = str(datetime.datetime.fromtimestamp(event_start))
    body = 'There will be a viewable satellite event on: ' + date
    message = twilio_client.messages.create(body=body, from_=twilio_number, to=my_number)


def beep(stop_event):
    pygame.mixer.init()
    pygame.mixer.music.load('notification.mp3')
    while not stop_event.is_set():
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue


def flash_led(stop_event):
    while not stop_event.is_set():
        GPIO.output(chan_list, (True, True, True))
        time.sleep(1)
        GPIO.output(chan_list, (False, False, False))
        time.sleep(1)
    # exit
    GPIO.output(chan_list, (False, False, False))


def start_alerts(event_time):
    stop_event = threading.Event()

    t_beep = threading.Thread(target=beep, kwargs={"stop_event": stop_event})
    t_beep.start()
    t_led = threading.Thread(target=flash_led, kwargs={"stop_event": stop_event})
    t_led.start()

    # sleep until the event if the event hasn't happened, else end
    if event_time - time.time() > 0:
        time.sleep(event_time - time.time())

    stop_event.set()
    t_beep.join()
    t_led.join()


def event_scheduler(account_sid, auth_token, my_number, events):
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
        alert_time = event['start'] - datetime.timedelta(seconds=900).total_seconds()

        print('Scheduled event for ', datetime.datetime.fromtimestamp(alert_time))
        print('Event will occur in ', alert_time-time.time(), ' seconds\n')

        # schedule the sms alert
        s.enterabs(time=alert_time, action=send_text, priority=1,
                   kwargs={'account_sid': account_sid, 'auth_token': auth_token, 'my_number': my_number,
                           'event_start': event['start']})
        # schedule the led/audio alerts
        s.enterabs(time=alert_time, action=start_alerts, priority=1, kwargs={'event_time': event['start']})
    s.run(blocking=True)

    GPIO.cleanup(chan_list)
