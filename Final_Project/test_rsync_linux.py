#! /usr/bin/env python3

# Instructions:
# To get this to work setup pubkey (passwordless) authentication
# by following these instructions:
# https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md

# Run the script.
# Tip: You may need to run the rsync command once so the remote becomes
# a known host

import json
import sys
import traceback
from subprocess import call

with open('password.json') as json_data:
    d = json.load(json_data)
    try:
        ip = d['rsync']['ip']
        username = d['rsync']['username']

    except:
        print('\nError in reading login_keys.json\nDisplaying trace:\n\n')
        print(traceback.format_exc())
        sys.exit(1)

command = 'rsync -av --delete -e ssh ./testFile.txt ' + username + '@' + ip + ':~/rsyncTests/'
print(command)

call(command.split(" "));


# rsync -av --delete -e ssh ./testFile.txt stephen@localhost:~/rsyncTests
