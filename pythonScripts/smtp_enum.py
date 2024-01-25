#!/usr/bin/python
import sys 
import socket
if len(sys.argv) != 3:
    print ("Usage ./python_enump.py <IP> <usr>")
    exit(0)
ip=sys.argv[1]
user=sys.argv[2]
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect=s.connect((ip,25))
banner=s.recv(1024) 
print banner
s.send('VRFY'+ user + '\r\n' )
results=s.recv(1024)
print result
s.close()
