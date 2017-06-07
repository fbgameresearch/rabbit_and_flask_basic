#!/bin/bash
sh -c 'docker-compose down'
sh -c 'docker-compose up -d --build'
# sh -c './publisher_daemon.py'
