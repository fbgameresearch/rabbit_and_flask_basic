#!/usr/bin/env python
import pika
import json
import redis

r = redis.StrictRedis(host='redis')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))

channel = connection.channel()

channel.exchange_declare(exchange='util_data',
                         type='fanout')

result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

channel.queue_bind(exchange='util_data',
                   queue=queue_name)

def callback(ch, method, properties, body):
    print(" [x] Received message")
    data = json.loads(body)
    # print("ID: {}".format(str(data[0]['host_id'])))
    r.set("ram",str(data[0]['general_ram_util']))
    r.set("cpu",str(data[0]['general_cpu_util']))
    r.set("net",str(data[0]['general_net_util']))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
