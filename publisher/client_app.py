#!/usr/bin/env python
import threading
import pika
import ps_obtain
import json

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


def every_two_seconds():
    threading.Timer(2.0, every_two_seconds).start()
    data = {
        "id": 1,
        "ram": ram_v(),
        "cpu": cpu_v(),
        "net": net_v()}
    channel.basic_publish(exchange='util_data',
                          routing_key='',
                          body=json.dumps(data))


every_two_seconds()
