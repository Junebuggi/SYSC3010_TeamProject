#Source: https://pymotw.com/2/socket/udp.html

#Import Packages
import socket, sys, time

#Initializing and setting Port and socket
textport = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = ('', port)
s.bind(server_address)

#Repeat
while True:
    #Receive data and print to screen if it is not length 0
    print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop " % port)
    #Address is of sender, buf is string sent
    buf, address = s.recvfrom(port)
    if not len(buf):
        #If length 0, exit while loop
        break
    print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))

#Shutdown Socket
s.shutdown(1)