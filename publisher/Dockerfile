FROM ubuntu:latest

WORKDIR /usr/src/app

RUN sh -c "apt-get update ; apt-get install docker.io -y ; apt-get -y install python-pip"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ./docker-entrypoint.sh
