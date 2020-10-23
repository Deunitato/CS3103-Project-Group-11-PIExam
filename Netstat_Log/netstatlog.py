#!/usr/bin/env python3

import os
import sys
import socket
import psutil
import atexit
from datetime import datetime
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from time import sleep

examTime = 10
filename = "./data/log.txt"

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}

def writeTxt():
    file = open(filename, "a+")
    file.write("\nTime:" + str(datetime.now().time()) + "\n")
    return file

def main():

    file = writeTxt()

    templ = "%-5s %-30s %-30s %-13s %-6s %s"
    file.write(templ % (
        "Proto", "Local address", "Remote address", "Status", "PID",
        "Program name"))
    file.write("\n")

    proc_names = {}
    for p in psutil.process_iter(['pid', 'name']):
        proc_names[p.info['pid']] = p.info['name']
    for c in psutil.net_connections(kind='inet'):
        laddr = "%s:%s" % (c.laddr)
        raddr = ""
        if c.raddr:
            raddr = "%s:%s" % (c.raddr)
        file.write(templ % (
            proto_map[(c.family, c.type)],
            laddr,
            raddr or AD,
            c.status,
            c.pid or AD,
            proc_names.get(c.pid, '?')[:15],
        ))
        file.write("\n")

def setTime(time):
    examTime = time

@atexit.register
def saveEndTime():
    print("exit called")
    file = open(filename, "a+")
    file.write("\n\n\nTime completed: " + str(datetime.now().time()) + "\n")

if __name__ == '__main__':
    # print('Number of arguments: {}'.format(len(sys.argv)))
    # print('Argument(s) passed: {}'.format(str(sys.argv)))
    if(len(sys.argv) < 3):
        raise Exception("Too little arguments parsed")
    args = sys.argv
    try:
        examTime = int(args[1])
        logInterval = int(args[2])
    except:
        print("Wrong input format")

    # Reset log file
    filename = "./data/log.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file = open(filename, "w+")

    counter = 0
    while counter != examTime:
        main()
        sleep(logInterval)
        counter = counter + logInterval
