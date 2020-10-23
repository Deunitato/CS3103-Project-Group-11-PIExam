"""
Main Script
    - Video Streaming (Background)
    - Netstat Logging (Background)
    - Test Administration
"""

from CLI_Questions import Questionable 
import subprocess
import signal
import os
from datetime import datetime

def main():

    # Exam Script
    examLength = input("Enter Exam length (Secs):")
    interval = input("Enter Log interval (Secs):")
    print("Total Exam Length: " + str(examLength) + "sec\n" + "Logging interval: " + str(interval) + "\n" )

    #netstatCLI = "python3 Netstat_Log/netstatlog.py " + str(examLength) + " " + str(interval)

    netstat = subprocess.Popen(["python3 Netstat_Log/netstatlog.py " + str(examLength) + " " + str(interval)], shell=True, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Open background process for video streaming
    vidStream = subprocess.Popen(["raspivid -o - -t 0 -n -w 320 -h 240 -fps 30| cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8000/}' :demux=h264"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True, preexec_fn=os.setsid, shell=True)

    subprocess.run("python3 CLI_Questions/Questionable.py", shell=True)

    # Save final time
    #file = open("./Data/log.txt", "a+")
    #file.write("\n\n\nTime completed:" + str(datetime.now().time()) + "\n")

    #print("written to file")

    # Cleanup
    os.killpg(os.getpgid(vidStream.pid), signal.SIGTERM)
    print("\n================================================\n")
    print("                   End of Quiz                    \n")
    print("================================================\n")
    print("Please wait while cleanup in progress...")

    vidStream.wait()
    netstat.wait()
    print("DONE")

if __name__ == "__main__":
    main()
