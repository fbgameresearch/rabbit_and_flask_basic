#!/usr/bin/env python
import threading
import pika
import ps_obtain
import json
import docker
import uuid

docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))

channel = connection.channel()

channel.exchange_declare(exchange='util_data',
                         type='fanout')


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
    inf = client.containers.list()
    data = []
    data.append({
        "host_id": uuid.uuid4(),
        "general_ram_util": ram_v(),
        "general_cpu_util": cpu_v(),
        "general_net_util": net_v()})
    for i in range(len(inf)):
        data.append(inf[i].stats(stream=False))
    respond = json.dumps(data)
    return respond

def every_two_seconds():
    threading.Timer(2.0, every_two_seconds).start()
    per_docker_data = per_docker()
    channel.basic_publish(exchange='util_data',
                          routing_key='',
                          body=json.dumps(data))


every_two_seconds()
