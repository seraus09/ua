#!/usr/bin/env python3
import time
import os
import os.path
import concurrent.futures
import sys

def received():
    """Return generator the list interfaces """
    interfaces = "/sys/class/net/"
    devices = os.listdir(interfaces)
    for dev in devices:
        received = "/sys/class/net/{0}/statistics/rx_bytes".format(dev)
        yield received

def sender():
     interfaces = '/sys/class/net/'
     devices = os.listdir(interfaces)
     for dev in devices:
         sender = "/sys/class/net/{0}/statistics/tx_bytes".format(dev)
         yield sender


def transmissionrate(a):
    """Return the transmisson rate of a interface under linux
    dev: devicename
    direction: rx (received) or tx (sended)
    timestep: time to measure in seconds
    """
    timestep = 2
    f = open(a, "r")
    bytes_before = int(f.read())
    f.close()
    time.sleep(timestep)
    f = open(a, "r")
    bytes_after = int(f.read())
    f.close()
    speed = lambda x, y: (x - y) / timestep
    results1 = speed(bytes_after, bytes_before)
    return results1


def thread_recived():
   thread = concurrent.futures.ThreadPoolExecutor(2)  # number Thread
   interfaces = []
   for i in received():
       interfaces.append(i)
   result = thread.map(transmissionrate,interfaces)
   return result

def thread_sender():
    thread = concurrent.futures.ThreadPoolExecutor(2) # number Thread
    interfaces = []
    for i in sender():
        interfaces.append(i)
    result = thread.map(transmissionrate,interfaces)
    return result

def main_recived():
    for a  in  thread_recived():
        convert = lambda a: int(a / 1000 / 1000 * 8)
        res = convert(a)
        yield res

def main_sender():
    for a  in  thread_sender():
        convert = lambda a: int(a / 1000 / 1000 * 8) # conversion to Mb/s
        res = convert(a)
        yield res

def result():
    max_speed_received = 50 # Max speed incoming traffic
    max_speed_sender  = 50 # Max speed outgoing traffic
    warning_speed = 20
    for received in main_recived():
        if received >= max_speed_received:
            print ("CRITICAL", received," Mb/s incoming traffic")
            sys.exit(2)
        elif received>=warning_speed:
            print ("WARNING", received,"Mb/s incoming traffic")
            sys.exit(3)    
    for sender in main_sender():
        if sender >= max_speed_sender:
            print ("CRITICAL",sender,"Mb/s outgoing traffic")
            sys.exit(2)
        elif sender >= warning_speed:
            print ("WARNING", sender,"Mb/s outcoming traffic")
            sys.exit(3)        
    else:
        print("OK" ,received,"Mb/s incoming traffic",sender,"Mb/s outcoming traffic")
        sys.exit(0)
if __name__ == '__main__':
    result()

