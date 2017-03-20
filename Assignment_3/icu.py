#! /usr/bin/env python3

import sys
import argparse
import datetime
import twilio

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
    exit()
except Exception as e:
    print("ERROR: " + str(e))
    exit()

line = f.readline()

while "st_username : " not in line and line != "":
    line = f.readline()

try:
    username = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Space-Track username in 'login_keys.txt'")
    exit()

while "st_password : " not in line and line != "":
    line = f.readline()

try:
    password = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Space-Track password in 'login_keys.txt'")
    exit()

while "accountSID : " not in line and line != "":
    line = f.readline()

try:
    accountSID = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Twilio accountSID in 'login_keys.txt'")
    exit()

while "authToken : " not in line and line != "":
    line = f.readline()

try:
    authToken = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Twilio authToken in 'login_keys.txt'")
    exit()


# --------------------------------------------------------------------------------

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

    date = datetime.datetime.now()

    # Get TLE orbital elements
    baseURL = 'https://www.space-track.org'

    d1 = date + datetime.timedelta(days=1)

    print('Connecting...')


if __name__ == "__main__":
    try:
        main()
    except:
        print('')
        sys.exit(1)
