#! /usr/bin/env python3

import sys
import argparse
from time import sleep
import datetime
from twilio.rest import TwilioRestClient

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

try:
    f = open("login_keys.txt", "r")
except FileNotFoundError as inst:
    print("The file 'login_keys.txt' was not found")
    sys.exit(1)
except Exception as e:
    print("ERROR: " + str(e))
    sys.exit(1)

line = f.readline()

while "st_username : " not in line and line != "":
    line = f.readline()

try:
    username = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Space-Track username in 'login_keys.txt'")
    sys.exit(1)

while "st_password : " not in line and line != "":
    line = f.readline()

try:
    password = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Space-Track password in 'login_keys.txt'")
    sys.exit(1)

while "accountSID : " not in line and line != "":
    line = f.readline()

try:
    accountSID = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Twilio accountSID in 'login_keys.txt'")
    sys.exit(1)

while "authToken : " not in line and line != "":
    line = f.readline()

try:
    authToken = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Twilio authToken in 'login_keys.txt'")
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
