#! /usr/bin/env python3

import sys
import argparse
from time import sleep
import datetime
import json
import traceback
import requests
import time
from event_scheduler import event_scheduler

# -------------------------- Get keys and credentials ----------------------------
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


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Artificial satellite monitor gateway that queries Space-Track and NOAA')

    # Add arguments to the parser
    parser.add_argument('-z', required=True, help='zipcode of viewing area')
    parser.add_argument('-s', required=True, help='NORAD ID of satellite to view')

    # Store arguments into variable
    args = parser.parse_args()

    zipcode = args.z
    noradId = args.s

    clearDays = []

    try:
        payload = {'cnt': 16, 'zip': [zipcode + ',us'], 'appid': appID}
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily', params=payload)
        parsed = json.loads(r.content)

        latitude = (parsed['city']['coord']['lat'])
        longitude = (parsed['city']['coord']['lon'])

        for item in parsed['list']:
            if item['clouds'] <= 20:
                temp = ((time.localtime(item['dt'])))
                clearDays.append(datetime.date(temp.tm_year, temp.tm_mon, temp.tm_mday))
    except:
        print("\nError querying weather api\nDisplaying trace:\n\n")
        print(traceback.format_exc())
        sys.exit(1)

    # The following line of code shows the list of clear days returned and the required lat and long
    print('Found ' + str(len(clearDays)) + ' clear days at ' + str(longitude) + ' ' + str(latitude))

    # Get current date and time
    date = datetime.datetime.now()

    # Get TLE orbital elements
    baseURL = 'https://www.space-track.org'

    d1 = date + datetime.timedelta(days=1)

    # Contains next five viewable date/times
    # Include sat position, direction of travel, and duration of visibility
    events = {}

    # Schedule event notifications
    event_scheduler(accountSID, authToken, myNumber, events)


if __name__ == "__main__":
    try:
        main()
    except:
        print('')
        sys.exit(1)
