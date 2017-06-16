#!/usr/bin/env python
import pika
import json
import psycopg2
import time
import logging

# create logger with 'spam_application'
logger = logging.getLogger('consumer_app')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('debug_logs.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))

channel = connection.channel()

channel.exchange_declare(exchange='util_data',
                         type='fanout')

result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

channel.queue_bind(exchange='util_data',
                   queue=queue_name)


def callback(ch, method, properties, body):
    logger.info('Received data from rabbitmq')
    try:
        try:
            conn = psycopg2.connect(
                "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
        except:
            logger.error('Unable to esetablish connection with database')
        cur = conn.cursor()
        data = json.loads(body)
        ts = time.time()
        host_id = data[0]['host_id']
        for indx in range(len(data)):
            if indx == 0:
                try:
                    general_ram_util = data[indx]['general_ram_util']
                    general_cpu_util = data[indx]['general_cpu_util']
                    general_net_util = data[indx]['general_net_util']
                except:
                    logger.error('Failed parsing data from general json')
                try:
                    cur.execute("INSERT INTO ram (host_id, name, time, usage_ram) VALUES (%s, %s, %s, %s)",
                                (host_id, "root", ts, general_ram_util))
                    cur.execute("INSERT INTO cpu (host_id, name, time, usage_cpu) VALUES (%s, %s, %s, %s)",
                                (host_id, "root", ts, general_cpu_util))
                    cur.execute("INSERT INTO net (host_id, name, time, rx_bytes) VALUES (%s, %s, %s, %s)",
                                (host_id, "root", ts, general_net_util))
                except:
                    logger.error('Failed inserting general data to database')
            else:
                try:
                    name = data[indx]['name']
                    read_time = data[indx]['read']
                    ram_usage = data[indx]['memory_stats']['usage']
                    ram_limit = data[indx]['memory_stats']['limit']
                    cpu_usage = data[indx]['cpu_stats']['cpu_usage']['total_usage']
                    net_rx = data[indx]['networks']['eth0']['rx_bytes']
                    net_tx = data[indx]['networks']['eth0']['tx_bytes']
                except:
                    logger.error(
                        'Failed parsing data from docker-specific json')
                try:
                    cur.execute("INSERT INTO ram (host_id, name, time, usage_ram, limit_ram) VALUES (%s, %s, %s, %s, %s)",
                                (host_id, str(name), int(ts), str(ram_usage / ram_limit), str(ram_limit)))
                    cur.execute("INSERT INTO cpu (host_id, name, time, usage_cpu) VALUES (%s, %s, %s, %s)",
                                (host_id, str(name), str(ts), str(cpu_usage)))
                    cur.execute("INSERT INTO net (host_id, name, time, rx_bytes, tx_bytes) VALUES (%s, %s, %s, %s, %s)",
                                (host_id, str(name), str(ts), str(net_rx), str(net_tx)))
                except:
                    logger.error(
                        'Failed inserting docker-specific data to database')
        conn.commit()
        cur.close()
        conn.close()
    except:
        logger.error('Fatal error in the process, passing')


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
