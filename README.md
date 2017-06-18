# Local development (bash required)

##### Above system serves as a central server for gathering data sent via AMQP. Server is built on docker-compose, and a external client that produces data to the server is dockerized as well.

## Prerequirements

##### Clone repository:
```
git clone https://github.com/spekulant/rabbit_and_flask_basic.git
cd rabbit_and_flask_basic
```
##### Before you start installation, make sure that required system packages are installed on your machine:

* docker
* docker-compose

For Docker installation instructions and all Docker related issues refer to official [Docker Docs](https://docs.docker.com/)

## Building central server (aggregator, database and api server)

Build project from the main catalog using the command below, you might need to go up `cd ..` in order for the command to work.

```
docker-compose up --build
```
* Visit [http://localhost:5000/](http://localhost:5000/) to check if the build went as planned.
* Visit [http://localhost:5000/documentation](http://localhost:5000/documentation) to see the API endpoints documentation.
* Visit [http://localhost:5000/monitor](http://localhost:5000/monitor) to see the basic interface.
* Visit [http://localhost:15672/](http://localhost:15672/) to see how the packages are flying around. (login:guest / password:guest)

## Building external client (utilization report publisher)
It's super easy to connect new client to the server. I've created another repository where you have a docker-compose with single container serving as a agent for the main application. The only thing you have to keep in mind is the remote address of the main application which you have to type inside the docker-compose file under "environment" section

```
cd ..
git clone https://github.com/spekulant/external_publisher.git
cd external_publisher
docker-compose up --build
```
### Rebuilding

You have to re-build the project every time the code and/or requirements change. In such case, when it comes to `central server` run:
```
docker-compose down
docker-compose up --build
```
When it comes to `publisher` container you have to `kill` it and `rm` it
```
docker kill report_publisher
docker rm report_publisher
docker run --net=host -v /var/run/docker.sock:/var/run/docker.sock --name=publisher -d report_publisher
```
### Inspecting logs

```
docker-compose logs -f api
```
Use `rabbit`, etc. instead of web for other services logs.

### further documentation
- contents of the package sent from each client https://gist.github.com/spekulant/1812788f8505fa521eab3e1bf2f85897

#### external ports
- rabbit *15672* and *5672*
- redis *6379*
- flask api *5000*
