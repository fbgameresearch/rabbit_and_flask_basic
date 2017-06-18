#!/bin/bash
set -e
sh -c './wait-for-it.sh dbpostgres:5432 -t 30'
# sh -c 'cd static; npm install ; chmod -R 555 node_modules ; cd ..'
exec "$@"
