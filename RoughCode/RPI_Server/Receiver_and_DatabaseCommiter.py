#Source: https://pymotw.com/2/socket/udp.html
#Source: https://www.tutorialspoint.com/python/python_database_access.htm

#Author: Abeer Rafiq
#Modified: 10/24/2019

#Importing Packages
import socket, sys, time
import RPi.GPIO as GPIO
import sqlite3
from datetime import datetime, date

#Initializing GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) #Blue LED
GPIO.setup(4, GPIO.OUT) #Green LED

#Function to blink a certain Pin
def blink(pin):
    GPIO.output(pin, True)  
    time.sleep(1)  
    GPIO.output(pin, False)  
    time.sleep(1)  
    return

#Intializing and setting sockets and ports
textport = sys.argv[1]
port = int(textport)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('', port)
s.bind(server_address)

#Connecting to the database
dbconnect = sqlite3.connect("/home/pi/Documents/Team_Project/dataBases/plantNurseryDB.db");
dbconnect.row_factory = sqlite3.Row;
cursor = dbconnect.cursor();


#Repeat
while True:
    #Waiting to recieve data
    #Address of sender stored in address and string sent is stored in buf
    print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop " % port)
    buf, address = s.recvfrom(port)
    
    if not len(buf):
        #If string length 0 is sent, there is likely an error so exit while loop
        #Also blink Blue LED to represent an error
        blink(4)
        break
    else:
        #Print recieved string and blink Green LED to represent data being recieved succesfully
        print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))
        blink(17)
        
        #Extract data ignoring characters but keep decimals
        data = buf.split(",")
        data[0] = ''.join(c for c in data[0] if c.isdigit()) #PotID
        data[1] = ''.join(c for c in data[1] if (c.isdigit() | (c == "."))) #Room Temperature
        data[2] = ''.join(c for c in data[2] if (c.isdigit() | (c == "."))) #Room Humidity
        
        #get date and time
        tdate = str(date.today())
        ttime = str(datetime.now().strftime("%H:%M:%S"))
        
        #Info to be inserted in database 
        tempSQL = "insert into sensorData values (" + data[0] + ", 'Raspberry Pi', " + "'Room Temperature', " + data[1] + ", '" + tdate + "', '" + ttime + "')"
        humiditySQL = "insert into sensorData values (" + data[0] + ", 'Raspberry Pi', " + "'Room Humidity', " + data[2] + ", '" + tdate + "', '" + ttime + "')"    
  
        try:
            #Execute the SQL command and commit changes in database
            cursor.execute(tempSQL)
            cursor.execute(humiditySQL)
            dbconnect.commit();
        except:
            #Rollback in case there is any error
            db.rollback()


#Shutdown Socket
s.shutdown(1)
#Close Database
db.close()



