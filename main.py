from CLI_Questions import Questionable 
from subprocess import call

with open('Netstat_Log/netstatlog.py', 'w') as f:
   call(['python', 'Netstat_Log/netstatlog.py'], bash = True)
Questionable.main()
