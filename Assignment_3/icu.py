#! /usr/bin/env python3

import argparse
import datetime
import json
import sys
import time
import traceback
import math
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
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Artificial satellite monitor gateway that queries Space-Track and NOAA')

    # Add arguments to the parser
    parser.add_argument('-z', required=True, help='zipcode of viewing area')
    parser.add_argument('-s', required=True, help='NORAD ID of satellite to view')

    # Store arguments into variable
    args = parser.parse_args()

    zipcode = args.z
    norad_id = args.s

    clear_days = []

    try:
        payload = {'cnt': 16, 'zip': [zipcode + ',us'], 'appid': appID}
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily', params=payload)
        parsed = r.json()

        latitude = (parsed['city']['coord']['lat'])
        longitude = (parsed['city']['coord']['lon'])

        for item in parsed['list']:
            if item['clouds'] <= 20:
                temp = time.localtime(item['dt'])
                clear_days.append(datetime.date(temp.tm_year, temp.tm_mon, temp.tm_mday))
    except:
        print("\nError querying weather api\nDisplaying trace:\n\n")
        print(traceback.format_exc())
        sys.exit(1)

    # The following line of code shows the list of clear days returned and the required lat and long
    print('Found ' + str(len(clear_days)) + ' clear days at ' + str(longitude) + ' ' + str(latitude))
    print('\n' + zipcode + ' Coordinates: \nLongitude: ' + str(longitude) + '\nLatitude: ' + str(latitude))

    # Get current date and time
    date = datetime.datetime.now()

    # Get TLE orbital elements
    base_url = 'https://www.space-track.org'
    TLE = []

    try:
        s = requests.Session()
        payload = {'identity': username, 'password': password}
        r = s.post(base_url + '/ajaxauth/login', data=payload)
        r = s.get('https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/25544/orderby/ORDINAL asc/limit/1/metadata/false')
        #r = s.get(base_url + '/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/" + norad_id + "/ORDINAL/1/        
        parsed = r.json()
        TLE.append((parsed[0]['TLE_LINE0']))
        TLE.append((parsed[0]['TLE_LINE1']))
        TLE.append((parsed[0]['TLE_LINE2']))
        print('\nSatellite TLE: \n' +TLE[0] + '\n' + TLE[1] + '\n' + TLE[2] + '\n')


    except:        
        print("\nError querying space api\nDisplaying trace:\n\n")
        print(traceback.format_exc())
        sys.exit(1)

#pi ephem

    iss = ephem.readtle(TLE[0],TLE[1],TLE[2])

    obs = ephem.Observer()
    obs.lat = latitude
    obs.long = longitude
    for p in range(3):
        tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
        print('Date/Time (UTC)       Alt/Azim      Lat/Long     Elev')
        print ('======================================================')
        while tr < ts :
            obs.date = tr
            iss.compute(obs)
            print(str(tr) + ' | {:4.1f} {:5.1f} | {:4.1f} {:+6.1f} | {:5.1f}'.format(math.degrees(iss.alt), math.degrees(iss.az), math.degrees(iss.sublat), math.degrees(iss.sublong), iss.elevation/1000.))
            tr = ephem.Date(tr + 60.0 * ephem.second)
        print('')
        obs.date = tr + ephem.minute

    print('here')

    d1 = date + datetime.timedelta(days=1)

    # Contains next five viewable date/times
    # Include sat position, direction of travel, and duration of visibility
    events = {}

    # Schedule event notifications
    event_scheduler(account_sid, auth_token, my_number, events)


if __name__ == "__main__":
    try:
        main()
    except:
        print('')
        sys.exit(1)
