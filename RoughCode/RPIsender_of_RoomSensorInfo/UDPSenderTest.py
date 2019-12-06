#Source: https://pymotw.com/2/socket/udp.html

#Importing Packages
import socket, sys, time

#Initializing and setting host, port and socket
host = sys.argv[1]
textport = sys.argv[2]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

#Repeat
while 1:
    #Data is entered to send
    print ("Enter data to transmit: ENTER to quit")
    data = sys.stdin.readline().strip()
    if not len(data):
        #If nothing is sent, exit loop
        break
    #send data to server address
    s.sendto(data.encode('utf-8'), server_address)

#Shutdown socket
s.shutdown(1)

