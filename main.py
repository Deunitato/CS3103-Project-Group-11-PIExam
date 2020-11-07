"""
Main Script
    - Load exam config
    - Video Streaming (Background)
    - Netstat Logging (Background)
    - Test Administration
    - Sending Logs by SMTP
"""

import subprocess
import signal
import os
import csv
from datetime import datetime

csv.register_dialect('configDialect',delimiter='=',skipinitialspace=True,quoting=csv.QUOTE_ALL)

def readExamConfig():
    config = {}
    with open('./config/exam_config', 'r') as file:
        reader = csv.reader(file, dialect='configDialect')
        for line in reader:
            variable = line[0].strip()
            value = line[1].strip()
            config[variable] = value
        return config

def main():

    config = readExamConfig()

    print(f"Exam Length: {config['length']} seconds")

    try:
        os.makedirs("data")
    except FileExistsError:
        pass

    netstat = subprocess.Popen(["python3 core/netstat/netstat.py " + str(config['length']) + " " + str(config['interval'])], shell=True, stdin=None, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
    
    # Open background process for video streaming
    stream = subprocess.Popen(["raspivid -o - -t 0 -n -w 320 -h 240 -fps 30| cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8000/}' :demux=h264"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True, preexec_fn=os.setsid, shell=True)

    subprocess.run("python3 core/exam/exam.py", shell=True)

    # Cleanup
    os.killpg(os.getpgid(stream.pid), signal.SIGTERM)
    os.killpg(os.getpgid(netstat.pid), signal.SIGTERM)

    print("\n================================================\n")
    print("                   End of Quiz                    \n")
    print("================================================\n")
    print("Please wait while cleanup in progress...")

    stream.wait()
    netstat.wait()

    subprocess.run("python3 core/mail/mail.py " + str(config['teacherEmail']) + " " + str(config['teacherName']), shell=True)

    print("DONE")

if __name__ == "__main__":
    main()
