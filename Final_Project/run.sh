#! /usr/bin/env bash
./status_server.py &
./web_server.py &
./check_status.py &
