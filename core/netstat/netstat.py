#!/usr/bin/env python3

import os
import sys
import signal
import socket
import psutil
from datetime import datetime
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from time import sleep
from threading import Event

filename = "data/log.txt"

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}

exit = Event()

def resetLogfile():
    file = open(filename, "w")
    file.write("=================================================\n")
    file.write("=                  NETSTAT LOG                  =\n")
    file.write("=================================================\n")
    file.write("\nStarted on: " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n")
    file.close()

def cleanupLogfile():
    file = open(filename, "a+")
    file.write("\nCompleted on: " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n")
    file.close()

def record(logNumber):
    file = open(filename, "a+")
    file.write("\nID: " + str(logNumber) + "\n")
    file.write("Time: " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n")
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
    file.close()

def main():
    resetLogfile()
    counter = 0
    while (counter * logInterval) < examTime and not exit.is_set():
        record(counter + 1)
        exit.wait(logInterval)
        counter = counter + 1
    cleanupLogfile()

def quit(signo, _frame):
    exit.set()

if __name__ == '__main__':

    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG'+sig), quit)

    if(len(sys.argv) < 3):
        raise Exception("Too little arguments parsed")
    args = sys.argv
    try:
        examTime = int(args[1])
        logInterval = int(args[2])
    except:
        print("Wrong input format")

    main()

