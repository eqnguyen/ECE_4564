#! /usr/bin/env bash

# This script runs all the scripts required for the web server

./status_server.py &
./web_server.py &
./check_status.py &
