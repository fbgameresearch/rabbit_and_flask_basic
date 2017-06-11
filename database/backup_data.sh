#!/usr/bin/env bash

# pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
pg_dumpall -c -U postgres | gzip > util_as_of_`date +%d-%m-%Y"_"%H_%M_%S`.gz

# RESTORING DATA
# createdb dbname
# cat util_as_of_[date].gz | gunzip | psql -U postgres
