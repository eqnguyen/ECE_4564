#! /usr/bin/env python3

import event_scheduler
import time
import sys
import json
import traceback

f = ''
username = ''
password = ''
accountSID = ''
authToken = ''
myNumber = ''
appID = ''

with open('login_keys.json') as json_data:
    d = json.load(json_data)
    try:
        username = d['spacetrack']['username']
        password = d['spacetrack']['password']
        accountSID = d['twilio']['accountSID']
        authToken = d['twilio']['authToken']
	myNumber = d['twilio']['myNumber']
        appID = d['openweathermap']['appid']
    except:
        print("\nError in reading login_keys.json\nDisplaying trace:\n\n")
        print(traceback.format_exc())
        sys.exit(1)

schedule_time = time.time() + 10

events = [{"start":schedule_time}]

event_scheduler.event_scheduler(accountSID, authToken, myNumber, events)
