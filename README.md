# Local development

## Prerequirements

Before you start installation, make sure that required system packages are installed on your machine:

* docker
* docker-compose

For Docker installation instructions and all Docker related issues refer to official [Docker Docs](https://docs.docker.com/)

## Building

Clone repository:

```
git clone https://github.com/spekulant/rabbit_and_flask_basic.git
cd rabbit_and_flask_basic
```

Build project:

```
docker-compose build
docker-compose up -d
```

* Visit [http://localhost:5000/](http://localhost:5000/) to check if the build went as planned.

### Rebuilding

You have to re-build the project every time the code and/or requirements change. In such case run:
```
docker-compose down
docker-compose up --build
```

### Inspecting logs

```
docker-compose logs -f api
```
Use `rabbit`, etc. instead of web for other services logs.
