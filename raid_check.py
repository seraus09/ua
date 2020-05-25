#!/usr/bin/env python3
from pymdstat import MdStat
import os
import subprocess
import sys
import shlex
import re

def hardwareDetected():
# Detected hardware raid
    p1 = subprocess.Popen(shlex.split('lspci'),stdout=subprocess.PIPE)
    p2 = subprocess.Popen(shlex.split("grep -i  'RAID bus controller: Hewlett-Packard'"), stdin=p1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p1.stdout.close()
    output = p2.communicate()
    retcode = p2.returncode
    if retcode == 0:
       return True
    else:
       return False


def checkSsacli():
#If ssacli run return Ok, if not error
    try:
        if hardwareDetected():
           ssacli = subprocess.Popen(shlex.split('ssacli ctrl all show status'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
           output = ssacli.communicate()
           retcode = ssacli.returncode
           return True
        else:
            return False
    except:
        return False


def softwareDetected():
#Detected software raid and check it
    mds = MdStat()
    raid = mds.arrays() #Get all arrays
    for i in raid:
        if mds.config(i) == "chunks":
            continue
        elif mds.config(i) != "UU":
            return False
    else:
        return True

def find_disks():
#Find all disk in a system
    disks = list()
    reg = r"\b[n].{6,7}\b" #regx nmve
    list_disk = sorted(os.listdir('/sys/block'))
    a = str(list_disk)
    if "nvme" in a:
        for i in re.finditer(reg,a):
            disks.append('/dev/{}'.format(i.group(0)))
        return disks
    else:
        for dev in list_disk:
            try:
                with open('/sys/block/{}/device/type'.format(dev)) as f:
                    if f.read().strip() == '0':
                        disks.append('/dev/{}'.format(dev))


            except:
                continue

    return disks


def check_soft_disks():
#check dicks over smartctl
    disks = find_disks()
    for d in disks:
        cmd = '''sudo smartctl -H {0} | grep "SMART overall-health self-assessment test result:"| cut -f2 -d:'''.format(d)
        data = os.popen(cmd).read()
        res = data.splitlines()
        status = str(res)
        command = "smartctl -l error {0} | grep 'ATA Error Count'| cut -f2 -d:".format(d)
        results = os.popen(command).read()
        if "PASSED" not in status:
           return False, disks
        if results != '':
           return False
    else:
        return True, disks



def diskCount():
    try:
#Disk count of the hardware raid
        run_hpacucli  = subprocess.Popen(shlex.split('ssacli ctrl slot=0 pd all show status'),stdout=subprocess.PIPE)
        output = run_hpacucli.communicate()
        string = str(output)
        regex = r"\b[a-z]{10,15}\b"
        result = re.findall(regex,string )
        return len(result)
    except:
        return "No such file or directory 'ssacli', Was ssacli installed?"


def check_device_health():
# Check check_device_health hardware raid
   count = diskCount()
   for i in range(0,count):
       cmd = '''sudo smartctl -a -d cciss,{0} /dev/sda | grep "SMART overall-health self-assessment test result:"| cut -f2 -d:'''.format(i)
       data = os.popen(cmd).read()
       res = data.splitlines()
       status = str(res)
       command = "sudo smartctl -a -d cciss,{0}  -l error /dev/sda |grep 'ATA Error Count'| cut -f2 -d:".format(i)
       global results
       results = os.popen(command).read()
       if "PASSED" not in status:
           return False
       if results != '':
           return False
   else:
       return True


def checkRaid():
#Check  raid and disk
    try:
        if checkSsacli():
           run_hpacucli  = subprocess.Popen(shlex.split('ssacli ctrl slot=0 pd all show status'),stdout=subprocess.PIPE)
           output = run_hpacucli.communicate()
           result = str(output).replace('None', '').replace('b', '').strip('()')
           if "Failed" in result:
               return "RAID Error"
               return 2
           elif check_device_health():
               print ("Hardware RAID and DISKS are  OK ")
               return 0
           else:
               print('DISK failed', results)
               return 2

        elif softwareDetected() is None:
            return "Software Raid not found"

        elif softwareDetected():
            if check_soft_disks():
                print("Software RAID and DISKS are OK")
                return 0
            else:
                print('DISK FAILED')
                return 2
        else:
            print("RAID ERROR")
            return 2
    except:
        return "Error No such file or directory 'ssacli', Was ssacli installed?"



if __name__ == '__main__':
    sys.exit(checkRaid())
