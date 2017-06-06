# Local development (bash required)

##### Above system serves as a central server for gathering data sent via AMQP. Server is built on docker-compose, and a external client that produces data to the server is called from publisher/publisher_daemon.py

## Prerequirements

##### Clone repository:
```
git clone https://github.com/spekulant/rabbit_and_flask_basic.git
cd rabbit_and_flask_basic
```
##### Before you start installation, make sure that required system packages are installed on your machine:

* docker
* docker-compose
* virtualenv

##### The rest will be installed using what follows:

```bash
cd publisher
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For Docker installation instructions and all Docker related issues refer to official [Docker Docs](https://docs.docker.com/)

## Building

Build project from the main catalog using the command below, you might need to go up `cd ..` in order for the command to work.

```
./run_local.sh
```
* Visit [http://localhost:5000/](http://localhost:5000/) to check if the build went as planned.
* Afterwards, call `(./publisher/run_producer.sh &) &` in order to start producing utilization reports for the server we have just set up with docker-compose.
* Visit [http://localhost:15672/](http://localhost:15672/) to see how the packages are flying around. (login:guest / password:guest)

### Rebuilding

You have to re-build the project every time the code and/or requirements change. In such case run:
```
./run_local.sh
```

### Inspecting logs

```
docker-compose logs -f api
```
Use `rabbit`, etc. instead of web for other services logs.
### Troubleshooting
* In case you use windows and cannot run bash scripts *in order to build the project* run manually:
```bash
docker-compose up --build
```
* For Rebuilding manually do:
```bash
docker-compose down
docker-compose up --build
```
### further documentation
- contents of the package sent from each client https://gist.github.com/spekulant/1812788f8505fa521eab3e1bf2f85897
