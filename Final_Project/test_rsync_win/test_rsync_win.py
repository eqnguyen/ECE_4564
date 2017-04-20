#! /usr/bin/env python3

# Instructions:
# 1. You should already have the bin folder in your Final_Project directory
# 2. Add a testFile.txt you want to send
# 3. Add a password.json file with rsync.ip and rsync.username (pi)
# 4. Setup passwordless ssh - https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md
# 4a. go to bin directory in windows cmd prompt
# 4b. run cwrsync.cmd to configure ssh
# 4c. run "ssh-keygen.exe -t rsa -C "some text" then press enter 4 times
# 4d. Copy the text from bin/home/{user}/.ssh/id_rsa.pub to ~/.ssh/authorized_keys on your pi
# 5. Run this script
# 
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

command = './bin/rsync.exe -av --delete -e ./bin/ssh ./testFile.txt ' + username + '@' + ip + ':~/rsyncTests/'
print (command)

call(command.split(" "));