#!/usr/bin/python3
import socket
import docker
import sys
import os
import subprocess

class Host:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def check_socket(self):
    # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
        server_address = (self.host, self.port)
        try:
           sock.connect(server_address)
        except socket.error:
           return 1 # Return code error



def list_containers():
    """The List all docker containers which is in the system """
    client = docker.from_env()
    docker_list = [container.name for container in client.containers.list()]
    return docker_list


def containers_status():
    """Function for detecting container ports"""
    client = docker.from_env()
    for container in client.containers.list():
         ports = container.ports
         get_port = ((ports[(next(iter(ports)))])[0])['HostPort']
         yield container.name, container.status, get_port


def mysql_status():
    """Function for check mysql status """
    client = docker.from_env()
    for container in client.containers.list():
        name = container.name
        command = f"docker exec -i {name} mysqladmin ping"
        res = os.popen(command).read()
        if "alive" not in res:
            return False
    else:
        return True



def check_runContainer():
    """Function checks the container status """
    container1 = Host('localhost', 3310)
    container2 = Host('localhost', 3311)
    for a in container1 , container2:
       if  a.check_socket() == 1:
           print ('Container is DOWN!', [i for i in containers_status()])
           return 2
       elif mysql_status() == False:
           print ("Mysql not response!")
    else:
        print ("All OK ", [i for i in containers_status()])
        return 0

if __name__ == '__main__':
    sys.exit(check_runContainer())
