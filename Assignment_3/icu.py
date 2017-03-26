#! /usr/bin/env python3

import argparse
import datetime
import json
import math
import sys
import time
import traceback

import ephem
import requests
from event_scheduler import event_scheduler

# -------------------------- Get keys and credentials ----------------------------
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


def main():
    # -------------------------- Create argument parser ----------------------------
    parser = argparse.ArgumentParser(
        description='Artificial satellite monitor gateway that queries Space-Track and NOAA')

    # Add arguments to the parser
    parser.add_argument('-z', required=True, help='zipcode of viewing area')
    parser.add_argument('-s', required=True, help='NORAD ID of satellite to view')

    # Store arguments into variable
    args = parser.parse_args()

    zipcode = args.z
    norad_id = args.s

    # -------------------------- Get TLE orbital elements ----------------------------
    base_url = 'https://www.space-track.org'
    tle = []

    try:
        s = requests.Session()
        payload = {'identity': username, 'password': password}
        r = s.post(base_url + '/ajaxauth/login', data=payload)
        # r = s.get('https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/25544/orderby/ORDINAL asc/limit/1/metadata/false')
        r = s.get(base_url + '/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/' + norad_id + '/ORDINAL/1/')
        parsed = r.json()
        tle.append((parsed[0]['TLE_LINE0']))
        tle.append((parsed[0]['TLE_LINE1']))
        tle.append((parsed[0]['TLE_LINE2']))
        print('\nSatellite TLE: \n' + tle[0] + '\n' + tle[1] + '\n' + tle[2] + '\n')
    except:
        print("\nError querying space api\nDisplaying trace:\n\n")
        print(traceback.format_exc())
        sys.exit(1)

    # -------------------------- Get 15-day weather forecast ----------------------------
    clear_days = []

    try:
        payload = {'cnt': 15, 'zip': [zipcode + ',us'], 'appid': appID}
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily', params=payload)
        parsed = r.json()

        latitude = (parsed['city']['coord']['lat'])
        longitude = (parsed['city']['coord']['lon'])

        print(zipcode + ' Coordinates: \nLatitude: ' + str(latitude) + '\nLongitude: ' + str(longitude) + '\n')

        print('{:13}{:23}{:5}'.format('Date', 'Forecast', 'Clouds'))
        print('===========================================')

        for item in parsed['list']:
            temp = time.localtime(item['dt'])
            date = datetime.date(temp.tm_year, temp.tm_mon, temp.tm_mday)
            print(str(date) + ' | {:20} | {:<10}'.format(item['weather'][0]['description'],
                                                         str(item['clouds']) + ' %'))

            if item['clouds'] < 20:
                clear_days.append(date)

        print('\nThere are ' + str(len(clear_days)) + ' clear days in the next 15 days')
    except:
        print("\nError querying weather api\nDisplaying trace:\n\n")
        print(traceback.format_exc())
        sys.exit(1)

    # -------------------------- Get satellite ephemeris data ----------------------------
    iss = ephem.readtle(tle[0], tle[1], tle[2])

    obs = ephem.Observer()
    obs.lat = latitude
    obs.long = longitude

    visible = 0
    events = []
    while visible < 5 and len(clear_days) > 0:
        try:
            tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
        except ValueError:
            print("That satellite seems to always stay below your horizon")
            break;

        ob_year = (tr.triple()[0])
        ob_month = (tr.triple()[1])
        ob_day = (math.floor(tr.triple()[2]))
        ob_date = datetime.date(ob_year, ob_month, ob_day)
        old_tr = tr

        if clear_days.count(ob_date) > 0:
            print('\nDate/Time (UTC)       Alt/Azim      Lat/Long     Elev')
            print('======================================================')
            while tr < ts:
                obs.date = tr
                iss.compute(obs)
                print(str(tr) + ' | {:4.1f} {:5.1f} | {:4.1f} {:+6.1f} | {:5.1f}'.format(math.degrees(iss.alt),
                                                                                         math.degrees(iss.az),
                                                                                         math.degrees(iss.sublat),
                                                                                         math.degrees(iss.sublong),
                                                                                         iss.elevation / 1000.))
                tr = ephem.Date(tr + 60.0 * ephem.second)
            print('')
            obs.date = tr + ephem.minute
            visible = visible + 1
            tup = (old_tr, ts)
            events.append(tup)
        elif ob_date > clear_days[-1]:
            break;
        else:
            obs.date = ts + ephem.minute

    if visible < 5:
        print("There are less than 5 viewable events in the next 15 days")

    # Contains next five viewable date/times
    # Include sat position, direction of travel, and duration of visibility
    print(events)

    # -------------------------- Schedule event notifications ----------------------------
    # event_scheduler(account_sid, auth_token, my_number, events)


if __name__ == "__main__":
    try:
        main()
    except:
        print(traceback.format_exc())
        sys.exit(1)
