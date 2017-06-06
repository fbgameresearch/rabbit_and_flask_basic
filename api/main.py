from flask import Flask
import redis
import json

r = redis.StrictRedis(host='redis')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route("/util/cpu")
def cpu_with_json():
    response = {"cpu_util": str(r.get('cpu'))}
    return json.dumps(response)


@app.route("/util/ram")
def ram_with_json():
    response = {"ram_util": str(r.get('ram'))}
    return json.dumps(response)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
