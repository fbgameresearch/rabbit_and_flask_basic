#!/usr/bin/env python
import threading
import pika
import ps_obtain
import json
import docker
import uuid
import random as r

docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='fiware_main'))

channel = connection.channel()

channel.exchange_declare(exchange='util_data',
                         type='fanout')

hostid = int(r.random()*100000)

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
        data.append(inf[i].stats(stream=False))
    respond = json.dumps(data)
    # print('data sent')
    return respond

def every_two_seconds():
    threading.Timer(5.0, every_two_seconds).start()
    per_docker_data = per_docker()
    channel.basic_publish(exchange='util_data',
                          routing_key='',
                          body=per_docker_data)


every_two_seconds()
