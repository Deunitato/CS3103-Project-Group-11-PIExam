#!/usr/bin/env python3

# Copyright (c) 2009, Giampaolo Rodola'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import socket
from datetime import datetime
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from time import sleep

import psutil

examTime = 10

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}

def writeTxt():
    file = open("log.txt", "a+")
    file.write("\nTime:" + str(datetime.now().time()) + "\n")
    return file


def main():

    file = writeTxt()

    templ = "%-5s %-30s %-30s %-13s %-6s %s"
    # print(templ % (
    #     "Proto", "Local address", "Remote address", "Status", "PID",
    #     "Program name"))
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
        # print(templ % (
        #     proto_map[(c.family, c.type)],
        #     laddr,
        #     raddr or AD,
        #     c.status,
        #     c.pid or AD,
        #     proc_names.get(c.pid, '?')[:15],
        # ))
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

if __name__ == '__main__':
    counter = 0
    while counter != 5:
        main()
        sleep(5)
        counter = counter + 1