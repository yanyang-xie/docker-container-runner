#!/usr/bin/env python

import yaml 
import docker 
from jsonpath_rw import jsonpath, parse
import sys
import simplejson as json

d = docker.Client(base_url='unix://var/run/docker.sock', version="1.5")

try:
   stream = open(sys.argv[1])
except:
   print "no filename given, or incorrect file"
   sys.exit()

config = yaml.load(stream)
#global result_config

for key, values in config.items():
   print "processing {}".format(key)
 
   container = values.get("container", None)
   image = values.get("image", None)
   command = values.get("command", None)
   volumes = values.get("volumes", None)
   hostname = values.get("hostname", None)
   ports = values.get("ports", None)
   dep_env = values.get("dep_env", None)
   env = []


   # print ports
   #print "found image {}\n command {}\n volumes {}\n hostname {}\n ".format(image, command, volumes, hostname)
   # print "found {} {} {}".format(image, command, volumes)
   #print "ports:", ports

   env_var = None
   if dep_env:
      env_key = dep_env[0].split('=')[0]
      env_value = dep_env[0].split('=')[1]
      env_path = env_value.split('.')
      print env_value
      env_var = ["{}={}".format(env_key, config.get(env_path[0]).get(env_path[1]))]
      #env_item = "{}={}".format(env_key, values.get(env_path[0]).get(env_path[1]).get(env_path[2]))
      #print "dependent environment {}".format(env_item)

   c_ports = {}
   s_ports = {}

   for port in ports or []:
      parts = port.split(":")
      
      host_ip = ''
      host_port = ''

      if len(parts) == 1:
         container_port = parts[0]
      if len(parts) == 2:
         host_port = parts[0]
         container_port = parts[1]
      if len(parts) == 3:
         host_ip = parts[0]
         host_port = parts[1]
         container_port = parts[2]
      
      if not (container_port.endswith('tcp') or container_port.endswith('udp')):
         container_port += "/tcp" 

      c_ports[container_port] = {}
      s_ports[container_port] = [{'HostIp': '', 'HostPort': host_port}]

   print "c_ports = ", c_ports 
   print "s_ports = ", s_ports

   vols = {}
   binds = {}
   for volume in volumes or []:
      parts = volume.split(":")
      # host mount (e.g. /mnt:/tmp, bind mounts host's /tmp to /mnt in the container)
      if len(parts) == 2:
         vols[parts[1]] = {}
         binds[parts[0]] = parts[1]
         # docker mount (e.g. /www, mounts a docker volume /www on the container at the same location)
      else:
         vols[parts[0]] = {}

   print 'volumes = ', vols

   
   if container:
      try:
         result = d.start(container, port_bindings=s_ports, binds=binds)
      except Exception as ex:
         print ex
      continue

   container = d.create_container(image, command, environment=env_var, volumes=vols, ports=c_ports, detach=True)
   result = d.start(container, port_bindings=s_ports, binds=binds)
   
   print result

   details = d.inspect_container(container)
   
   config[key]['PortMapping'] = details["NetworkSettings"]["PortMapping"]
   print config[key]


print config

