FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN sh -c "apt-get update ; apt-get install docker.io -y ; apt-get -y install python-pip"


COPY . .
