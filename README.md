# Python-Scripts

getRadiusVPNLogs is specifically designed to:

1. grab the log file from a mapped drive 
2. parse out the needed text 
3. put it in a temporary file 
4. load that file into an e-mail 
5. send the email 
6. then delete the temporary file

Need to generalize it so all the hardcoded parameters can be input by the user. Need to make it more robust so on failure the script does not crash. (i.e. try/catch exceptions)
