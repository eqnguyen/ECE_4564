#! /usr/bin/env python3

# Instructions:
# 1. You should already have the bin folder in your test_rsync_win directory
# 2. Add a testFile.txt you want to send
# 3. Add a password.json file with rsync.ip and rsync.username (pi)
# 4. Setup passwordless ssh - https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md
# 4a. go to test_rsync_win directory in windows cmd prompt
# 4b. run cwrsync.cmd to configure ssh
# 4c. go to the test_rsync_win/bin director in windows command prompt
# 4d. run "ssh-keygen.exe -t rsa -C "some text" then press enter 4 times
# 4e. Copy the text from test_rsync_win/home/{user}/.ssh/id_rsa.pub to ~/.ssh/authorized_keys on your pi
# 5. You may have to start the rsync daemon on the pi with:
# 		sudo systemctl enable rsync
#		sudo systemctl start rsync
# 6. Run this script (from win cmd prompt you can enter "python test_rsync_win.py")
# 
# Tip: You may need to run the rsync command once (or type yes the 
# first time you run the script) so the remote becomes a known host

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