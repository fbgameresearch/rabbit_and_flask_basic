#!/usr/bin/env python
import threading
import pika
import ps_obtain
import json
import docker
import uuid
import random as r
import logging
import os

# create logger with 'spam_application'
logger = logging.getLogger('publisher_app')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('debug_logs.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))

channel = connection.channel()

channel.exchange_declare(exchange='util_data',
                         type='fanout')

hostid = int(r.random() * 100000)


def cpu_v():
    # return json.dumps({'utilization': ps_obtain.cpu_util_value()})
    return str(ps_obtain.cpu_util_value())


def ram_v():
    # return json.dumps({'utilization': ps_obtain.cpu_util_value()})
    # return json.dumps(ps_obtain.ram_util_percent())
    return str(ps_obtain.ram_util_percent())


def net_v():
    # return json.dumps(ps_obtain.net_util_value())
    return str(ps_obtain.net_util_value())


def per_docker():
    inf = docker_client.containers.list()
    data = []
    data.append({
        "host_id": hostid,
        "general_ram_util": ram_v(),
        "general_cpu_util": cpu_v(),
        "general_net_util": net_v()})
    for i in range(len(inf)):
        try:
            data.append(inf[i].stats(stream=False))
        except:
            logger.error('Unable to parse data from docker api')
    respond = json.dumps(data)
    return respond


def every_n_seconds(t=5.0):
    threading.Timer(t, every_n_seconds).start()
    per_docker_data = per_docker()
    channel.basic_publish(exchange='util_data',
                          routing_key='',
                          body=per_docker_data)

if int(os.environ['METACIRCULARITY'])==1:
    n = int(os.environ['INTERVAL'])
    logger.debug('using host_id %d' % hostid)
    every_n_seconds(n)
