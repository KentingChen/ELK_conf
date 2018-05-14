#!/bin/python
import socket, string, json, time
from argparse import ArgumentParser
from random import randrange


def Packer(randomIsON=True):
    if randomIsON:
        def rrange(length, min_i=0, max_i=10):
            return ''.join([str(randrange(min_i,max_i)) for i in range(length)])
        customerID = string.ascii_uppercase[randrange(0,26)]+str(rrange(1,min_i=1))+'*****'+str(rrange(3))
        message = {
            'LoginID':  str(randrange(1000,2000)),
            'CustomerID':  customerID,
            'RoleID': rrange(1,max_i=2)+rrange(1),
            'UserTerminal': '10.88.120.'+str(randrange(1,256)),
            'BranchNumber': '0'+rrange(3),
            'SystemID': 'L0'+rrange(1,max_i=6)
        }
    else:
        message = {
            'LoginID': 1988,
            'CustomerID':'A123456789',
            'RoleID':'02',
            'UserTerminal':'10.88.8.7',
            'BranchNumber':'0012',
            'SystemID':'02x3'
        }
    #print str(json.dumps(message,ensure_ascii=False))
    #return str(json.dumps(message,ensure_ascii=False))
    return json.dumps(message,ensure_ascii=False) + "\n"


def sendMSG(tHost, tPort, messageToSend):
    #tHost = 'daring.cwi.nl'  # The remote host
    #tPort = 50007  # The same port as used by the server
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tHost, int(tPort)))
    #s.sendall(str.encode(messageToSend))    
    s.send(messageToSend)
    #data = s.recv(1024)
    #print('Received', repr(data))
    #s.close()


def main():
    # Create command line arguments.
    parser = ArgumentParser(description='Parameters of DataSender(Python) for sending data to Logstash.', add_help=False)
    parser.add_argument('-h', action="store", dest='ls_host', default='127.0.0.1')
    parser.add_argument('-p', action="store", dest='ls_port', default=8877)
    #parser.add_argument('-l', action="store_false", dest='looping')
    parser.add_argument('-c', action="store", dest='count', default=1, type=int)
    parser.add_argument('-r', action="store", dest='repeat', default=1, type=int)
    parser.add_argument('-i', action="store", dest='interval', type=int)

    res = parser.parse_args()
   
    if res.count > 1024:
        print "Count [-c] parameters can NOT exceeds 1024, we will send 1024 times."
        res.count = 1024

    count = res.count  # store res.count to count for initializing.
    for i in range(res.repeat):
        res.count = count
        while res.count > 0:
            sendMSG(res.ls_host, res.ls_port, Packer())
            res.count -= 1
        if res.interval is not None:
            time.sleep(res.interval)


if __name__ == '__main__':
    main()
