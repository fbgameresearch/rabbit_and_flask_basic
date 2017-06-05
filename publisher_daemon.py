#!/usr/bin/env python
import docker

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
inf = client.containers.list()
for i in range(len(inf)):
    data.append(inf[i].stats(stream=False))
respond = json.dumps(data)
