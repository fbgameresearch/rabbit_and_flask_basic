from flask import Flask
import json
import logging
import psycopg2
from flask.ext.autodoc.autodoc import Autodoc


app = Flask(__name__)
auto = Autodoc(app)

# create logger with 'spam_application'
logger = logging.getLogger('API')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('debug_logs.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


@app.route('/')
@auto.doc()
def hello_world():
    return 'Flask Dockerized'


@app.route("/list-hosts")
@auto.doc()
def hosts_list():
    response = []
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
    except:
        logger.error('Unable to esetablish connection with database')
        return 400
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT host_id from ram")
        rows = cur.fetchall()
        for row in rows:
            response.append(row[0])
        cur.close()
        conn.close()
    except:
        logger.error('Unable to fetch host_id from ram table')
        return 400
    return json.dumps(response)


@app.route("/list-containers/<int:host_id>")
@auto.doc()
def containers_list(host_id):
    response = []
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
    except:
        logger.error('Unable to esetablish connection with database')
        return 400
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT name from ram where host_id=%d" % host_id)
        rows = cur.fetchall()
        for row in rows:
            response.append(row[0])
        cur.close()
        conn.close()
    except:
        logger.error('Unable to fetch host_id from ram table')
        return 400
    return json.dumps(response)


@app.route("/util/single/cpu/<int:host_id>")
@auto.doc()
def cpu_with_json(host_id):
    response = {}
    try:
        query = "SELECT name, usage_cpu FROM cpu where host_id=%d" % host_id
    except:
        logger.error('Wrong argument type for select request')
        return 400
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
        cur = conn.cursor()
    except:
        logger.error('Unable to esetablish connection with database')
        return 400
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            response[row[0]] = row[1]
        cur.close()
        conn.close()
    except:
        logger.error('Unable to execute select query on cpu table')
        return 400
    return json.dumps(response)


@app.route("/util/single/ram/<int:host_id>")
@auto.doc()
def ram_with_json(host_id):
    response = {}
    try:
        query = "SELECT name, usage_ram FROM ram where host_id=%d" % host_id
    except:
        logger.error('Wrong argument type for select request')
        return 400
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
        cur = conn.cursor()
    except:
        logger.error('Unable to esetablish connection with database')
        return 400
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            response[row[0]] = row[1]
        cur.close()
        conn.close()
    except:
        logger.error('Unable to execute select query on ram table')
        return 400
    return json.dumps(response)


@app.route("/util/single/net/<int:host_id>")
@auto.doc()
def net_with_json(host_id):
    response = {}
    try:
        query = "SELECT name, tx_bytes FROM net where host_id=%d" % host_id
    except:
        logger.error('Wrong argument type for select request')
        return 400
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
        cur = conn.cursor()
    except:
        logger.error('Unable to esetablish connection with database')
        return 400
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            response[row[0]] = row[1]
        cur.close()
        conn.close()
    except:
        logger.error('Unable to execute select query on net table')
        return 400
    return json.dumps(response)

#
# @app.route("/util/ram")
# def ram_with_json():
#     response = {"ram_util": str(r.get('ram'))}
#     return json.dumps(response)


@app.route('/documentation')
def documentation():
    return auto.html()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
