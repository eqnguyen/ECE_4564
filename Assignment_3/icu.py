#! /usr/bin/env python3

import sys
import argparse
import datetime


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

    # Change these
    username = 'username'
    password = 'password'

    d1 = date + datetime.timedelta(days=1)

    print('Connecting...')


if __name__ == "__main__":
    try:
        main()
    except:
        print('')
        sys.exit(1)
