#! /usr/bin/env python3

import sys
import argparse
from time import sleep
import datetime
from twilio.rest import TwilioRestClient
import json
import traceback

# import RPi.GPIO as GPIO

# Set pin mode to the numbers you can read off the pi
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
#
# Set up channel list
# chan_list = [13, 19, 26]  # 13 red, 19 green, 26 blue
# GPIO.setup(chan_list, GPIO.OUT)

# -------------------------- Get keys and credentials ----------------------------
f = ''
username = ''
password = ''
accountSID = ''
authToken = ''
appID = ''

with open('login_keys.json') as json_data:
    d = json.load(json_data)
    try:
        username = d['spacetrack']['username']
        password = d['spacetrack']['password']
        accountSID = d['twilio']['accountSID']
        authToken = d['twilio']['authToken']
        appID = d['openweathermap']['appid']
        print(appID)
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

    # Get current date and time
    date = datetime.datetime.now()

    # Get TLE orbital elements
    baseURL = 'https://www.space-track.org'

    d1 = date + datetime.timedelta(days=1)

    print('Connecting...')

    # Send sms text message
    twilioClient = TwilioRestClient(accountSID, authToken)
    twilioNumber = '+12403033631'
    myNumber = 'myCellNumber'

    body = 'Test'

    # message = twilioClient.messages.create(body=body, from_=twilioNumber, to=myNumber)

    # Flash LED
    # GPIO.output(chan_list, (True, True, True))
    # sleep(1)
    # GPIO.output(chan_list, (False, False, False))


if __name__ == "__main__":
    try:
        main()
    except:
        print('')
        sys.exit(1)
