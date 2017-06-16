#!/bin/bash
set -e
sh -c './wait-for-it.sh dbpostgres:5432 -t 30'
exec "$@"
