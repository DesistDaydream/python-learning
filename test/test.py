import socket


def getIP(domain):
    myaddr = socket.getaddrinfo(domain, 'http')
    print(myaddr)


getIP("www.baidu.com")
