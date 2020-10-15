from CLI_Questions import Questionable 
import subprocess
from datetime import datetime



def main():
   examLength = input("Enter Exam length (Secs):")
   interval = input("Enter Log interval (Secs):")
   print("Total Exam Length: " + str(examLength) + "sec\n" + "Logging interval: " + str(interval) + "\n" )
   netstatCLI = "python3 Netstat_Log/netstatlog.py " + str(examLength) + " " + str(interval)
   subprocess.run( netstatCLI + " & python3 CLI_Questions/Questionable.py", shell=True)

   # Save final time
   file = open("./Data/log.txt", "a+")
   file.write("\n\n\nTime completed:" + str(datetime.now().time()) + "\n")


if __name__ == "__main__":
    main()
