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
    # print(" [x] Received %r" % body)
    data = json.loads(body)
    # print("ID: {}".format(data['id']))
    r.set("ram",data['ram'])
    r.set("cpu",data['cpu'])
    r.set("net",data['net'])

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

# print('declared %s queue' % queue_name)
# print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
