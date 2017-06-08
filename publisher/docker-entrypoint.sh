#!/bin/bash
set -e
sh -c './wait-for-it.sh fiware_main:5672 -t 30'
exec "$@"
