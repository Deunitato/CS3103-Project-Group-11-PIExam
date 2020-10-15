from CLI_Questions import Questionable 
from subprocess import call

with open('Netstat_Log/netstatlog.py', 'r') as f:
   call(['python', 'Netstat_Log/netstatlog.py'])
Questionable.main()
