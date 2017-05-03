#! /usr/bin/env bash

# This script runs all the scripts required for the web server

./web_server.py &
./status_server.py &
./check_status.py > /dev/null &
./tcp_server.py &
