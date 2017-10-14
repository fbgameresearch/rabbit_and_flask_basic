FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
RUN sh -c "apt-get update ; apt-get install docker.io -y ; apt-get -y install python-pip"
RUN pip install -r requirements.txt

COPY . .
