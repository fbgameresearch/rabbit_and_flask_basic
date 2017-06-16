#!/bin/bash
set -e
sh -c './wait-for-it.sh rabbit:5672 -t 30'
sh -c 'python client_app.py'
exec "$@"
