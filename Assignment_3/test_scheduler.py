#! /usr/bin/env python3

import json
import sys
import time
import traceback

import event_scheduler

f = ''
username = ''
password = ''
account_sid = ''
auth_token = ''
my_number = ''
appID = ''

with open('login_keys.json') as json_data:
    d = json.load(json_data)
    try:
        username = d['spacetrack']['username']
        password = d['spacetrack']['password']
        account_sid = d['twilio']['accountSID']
        auth_token = d['twilio']['authToken']
        my_number = d['twilio']['myNumber']
        appID = d['openweathermap']['appid']
    except:
        print("\nError in reading login_keys.json\nDisplaying trace:\n\n")
        print(traceback.format_exc())
        sys.exit(1)

schedule_time = time.time() + 10

events = [{"start": schedule_time}]

event_scheduler.event_scheduler(account_sid, auth_token, my_number, events)
