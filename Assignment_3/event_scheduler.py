#! /usr/bin/env python3

import sched
import time, datetime
import threading

def eric_sms():
    print("Not implemented")


def eric_audio():
    print("Not implemented")


def eric_led():
    print("Not implemented")


def start_alerts():
    threading.Thread(target=eric_sms).start()
    threading.Thread(target=eric_audio).start()
    threading.Thread(target=eric_led).start()


def exit_led():
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