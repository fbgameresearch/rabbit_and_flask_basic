from flask import Flask, render_template, abort
import json
import logging
import psycopg2
from flask.ext.autodoc.autodoc import Autodoc
import re
from flask_cors import CORS, cross_origin

app = Flask(__name__)
auto = Autodoc(app)
CORS(app)

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
        return abort(400)
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
        return abort(400)
    # global_hosts_list=response
    return json.dumps(response)

@app.route("/monitor")
@auto.doc()
def monitor():
    count = []
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
    except:
        logger.error('Unable to esetablish connection with database')
        return abort(400)
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT host_id from cpu")
        hosts = cur.fetchall()
        for host in hosts:
            cur.execute("SELECT DISTINCT name from cpu where host_id=%d" % host)
            containers=cur.fetchall()
            count.append(len(containers))
        cur.close()
        conn.close()
        hosts_count = zip(hosts,count)
    except:
        logger.error('Unable to fetch host_id/name from cpu table')
        return abort(400)
    return render_template('hosts_list.html', hosts_count=hosts_count)


@app.route("/monitor/<url_host_id>")
@auto.doc()
def monitor_detail(url_host_id):
    host=int(re.search(r'\d+', url_host_id).group())
    names = []
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
    except:
        logger.error('Unable to esetablish connection with database')
        return abort(400)
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT name from cpu where host_id=%d" % host)
        containers=cur.fetchall()
        for name in containers:
            names.append(name)
        cur.close()
        conn.close()
    except:
        logger.error('Unable to fetch host_id/name from cpu table')
        return abort(400)
    return render_template('host_view.html', host_id=host, names=names)


@app.route("/list-containers/<int:host_id>")
@auto.doc()
def containers_list(host_id):
    response = []
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
    except:
        logger.error('Unable to esetablish connection with database')
        return abort(400)
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT name from ram where host_id=%d" % host_id)
        rows = cur.fetchall()
        for row in rows:
            response.append(row[0])
        if len(response)==1 and response[0]=="root":
            response = []
            cur.execute("SELECT DISTINCT name from cpu where host_id=%d" % host_id)
            rows = cur.fetchall()
            for row in rows:
                response.append(row[0])
        cur.close()
        conn.close()
    except:
        logger.error('Unable to fetch host_id from ram/cpu table')
        return abort(400)
    return json.dumps(response)


@app.route("/util/single/cpu/<int:host_id>")
@auto.doc()
def cpu_with_json(host_id):
    response = {}
    try:
        query = "SELECT name, usage_cpu FROM cpu where host_id=%d" % host_id
    except:
        logger.error('Wrong argument type for select request')
        return abort(400)
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
        cur = conn.cursor()
    except:
        logger.error('Unable to esetablish connection with database')
        return abort(400)
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            response[row[0]] = row[1]
        cur.close()
        conn.close()
    except:
        logger.error('Unable to execute select query on cpu table')
        return abort(400)
    return json.dumps(response)


@app.route("/util/single/ram/<int:host_id>")
@auto.doc()
def ram_with_json(host_id):
    response = {}
    try:
        query = "SELECT name, usage_ram FROM ram where host_id=%d" % host_id
    except:
        logger.error('Wrong argument type for select request')
        return abort(400)
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
        cur = conn.cursor()
    except:
        logger.error('Unable to esetablish connection with database')
        return abort(400)
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            response[row[0]] = row[1]
        cur.close()
        conn.close()
    except:
        logger.error('Unable to execute select query on ram table')
        return abort(400)
    return json.dumps(response)

@app.route("/util/single/net/<int:host_id>")
@auto.doc()
def net_with_json(host_id):
    response = {}
    try:
        query = "SELECT name, tx_bytes FROM net where host_id=%d" % host_id
    except:
        logger.error('Wrong argument type for select request')
        return abort(400)
    try:
        conn = psycopg2.connect(
            "dbname='utilization' user='pguser' host='dbpostgres' password='pguser'")
        cur = conn.cursor()
    except:
        logger.error('Unable to esetablish connection with database')
        return abort(400)
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            response[row[0]] = row[1]
        cur.close()
        conn.close()
    except:
        logger.error('Unable to execute select query on net table')
        return abort(400)
    return json.dumps(response)


@app.route("/static/charts.js")
@auto.doc()
def static_chart():
    return app.send_static_file('charts.js')

@app.route('/documentation')
def documentation():
    return auto.html()


if __name__ == "__main__":
    # global_hosts_list=[]
    app.run(debug=True, host='0.0.0.0')
