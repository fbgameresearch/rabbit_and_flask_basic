#!/bin/bash
set -e
sh -c './wait-for-it.sh redis:6379 -t 30'
exec "$@"
