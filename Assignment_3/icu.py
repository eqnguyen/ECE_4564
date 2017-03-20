#! /usr/bin/env python3

import sys
import argparse
import datetime

username = ''
password = ''
f = ''

try:
    f = open("space-track_login.txt", "r")
except FileNotFoundError as inst:
    print("The file 'space-track_login.txt' was not found")
    exit()
except Exception as e:
    print("ERROR: " + str(e))
    exit()

line = f.readline()
while "username : " not in line and line != "":
    line = f.readline()

try:
    username = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Twitter OAuth keys in 'api_keys.txt'")
    exit()

while "password : " not in line and line != "":
    line = f.readline()

try:
    password = line.split(' : ')[1].rstrip('\n')
except IndexError as inst:
    print("Could not find Twitter OAuth keys in 'api_keys.txt'")
    exit()


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
