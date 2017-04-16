#! /usr/bin/env python3

import json
import sys
import traceback

from ftpsync.targets import FsTarget
from ftpsync.ftp_target import FtpTarget
from ftpsync.synchronizers import UploadSynchronizer
from ftpsync.synchronizers import BiDirSynchronizer

with open('password.json') as json_data:
    d = json.load(json_data)
    try:
        username = d['host']['username']
        password = d['host']['password']
    except:
        print('\nError in reading login_keys.json\nDisplaying trace:\n\n')
        print(traceback.format_exc())
        sys.exit(1)

local = FsTarget("sync_test")
remote = FtpTarget("/sync_test", "192.168.1.10", username=username, password=password)
opts = {"force": False, "delete_unmatched": True, "verbose": 3, "dry_run": False}
s = UploadSynchronizer(local, remote, opts)
s.run()
