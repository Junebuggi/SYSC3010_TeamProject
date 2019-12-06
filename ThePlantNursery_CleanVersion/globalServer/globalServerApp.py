#Author: Abeer Rafiq
#Modified: 12/6/2019 11:40am

#Importing Packages
import socket, sys, time, json, sqlite3
import RPi.GPIO as GPIO
from datetime import datetime, date

#Creating a global server class
class GlobalServerApp:
    #The constructor
    def __init__(self, port, app_ip_addrs, debug):
        #Setting port
        self.__port = int(port)
        #Setting timeout/end time values
        self.__ack_timeout = 1
        self.__receive_timeout = 10
        self.__ack_endTime = 3
        #Setting whether to show print statement or not
        self.__DEBUG = debug
        #Setting socket to receive with a timeout set
        self.__soc_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_address = ('', self.__port)
        self.__soc_recv.bind(recv_address)
        #Setting socket/addresses to send to the room rpi and app
        self.__soc_send =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__app_addrs = (app_ip_addrs, self.__port)
        #Setting up led blinking  
        self.__receiveLED = 14  #error in receiving BLUE
        self.__sendLED = 15     #to show ack received GREEN
        self.__dberrorLED = 18     #to show error in updating DB RED
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__receiveLED, GPIO.OUT)
        GPIO.setup(self.__sendLED, GPIO.OUT)
        GPIO.setup(self.__dberrorLED, GPIO.OUT)
        #Setting up string for acknowldegements
        self.__ackstr = '{"opcode" : "0"}'
        #Setting up default threshold variables
        self.__defaultThresholdValue = 0
        self.__defaultLessGreaterThan = "<"
        #Setting database connections
        dbpath = '/home/pi/Documents/Team_Project/dataBases/plantNursery_DB.db'
        self.__dbconnect = sqlite3.connect(dbpath); 
        self.__dbconnect.row_factory = sqlite3.Row;
        self.__cursor = self.__dbconnect.cursor()        
        #Number of times to keep resending a msg if ack not received
        self.__numRetries = 1
        if (self.__DEBUG):
            print("\nGlobal Server Initialized")

    #Receives/returns buffer and sends ack 
    def receive(self):
        self.__soc_recv.settimeout(self.__receive_timeout)
        if (self.__DEBUG):
            print("\nWaiting to receive on port %d ... " % self.__port)
        #Keep Receiving
        while(1):
            #Try loading buffer, if error send no ack and blink receive LED to show error
            try:
                buf_noload, address = self.__soc_recv.recvfrom(self.__port)
                buf = json.loads(str(buf_noload))
                #Check to see if nothing received
                if len(buf) > 0:
                    if (self.__DEBUG):
                        print ("Received %s bytes from '%s': %s " % (len(buf), address[0], buf))
                    #Sending ack
                    self.__soc_send.sendto(self.__ackstr, (address[0], self.__port))
                    if (self.__DEBUG):
                        print ("Sent %s to %s" % (self.__ackstr, (address[0], self.__port)))
                    return (buf, buf_noload)
                else:
                    if (self.__DEBUG):
                        print("Nothing was Received")
                    #Blink receive LED to show error
                    self.blink(self.__receiveLED)
                    return None
            except (ValueError, KeyError, TypeError):
                if (self.__DEBUG):
                    print("Error in Loading Json String")
                #Blink receive LED to show error
                self.blink(self.__receiveLED)
                return None
            except socket.timeout:
                if (self.__DEBUG):
                    print("Receiving is Timed Out")
                return None            
    
    #To add user requested threshold entries into the db
    def updateUserThresholdsTable(self, threshold):
        potID = str(threshold.get("potID"))
        lessGreaterThan = str(threshold.get("lessGreaterThan"))
        thresholdValue = float(str(threshold.get("thresholdValue")))
        sensorType = str(threshold.get("sensorType"))
        tdate = str(date.today())
        ttime = str(datetime.now().strftime("%H:%M:%S"))
        #Insert thresholds into db
        mySQL = "INSERT INTO userThresholds VALUES ('" + potID + "', '" + sensorType + "', '" + str(thresholdValue) + \
                "', '" + lessGreaterThan + "', '" + str(tdate) + "', '" + str(ttime) + "')"    
        self.insertDBData(mySQL)
        #Reassign global server's instance threshold variables
        if sensorType == "light":
            self.__lightThreshold = thresholdValue
            self.__lightLessGreaterThan = lessGreaterThan
        elif sensorType == "soilMoisture":
            self.__soilMoistureThreshold = thresholdValue 
            self.__soilMoistureLessGreaterThan = lessGreaterThan
        elif sensorType == "roomTemperature":
            self.__roomHumidityThreshold = thresholdValue
            self.__roomHumidityLessGreaterThan = lessGreaterThan
        elif sensorType == "roomHumidity":
            self.__roomTemperatureThreshold = thresholdValue
            self.__roomTemperatureLessGreaterThan = lessGreaterThan
        if (self.__DEBUG):
            print("\nSet User Requested Thresholds")
        return
    
    #To add default threshold entries into the db
    def setDefaultThresholds(self, potID):
        print(potID)
        potID = str(potID)
        tdate = str(date.today())
        ttime = str(datetime.now().strftime("%H:%M:%S"))
        #Insert default thresholds into db
        mySQL = "INSERT INTO userThresholds VALUES ('" + potID + "', 'light', '" + \
                str(self.__defaultThresholdValue) + "', '" + self.__defaultLessGreaterThan + \
                "', '" + tdate + "', '" + ttime + "')"    
        self.insertDBData(mySQL)
        mySQL = "INSERT INTO userThresholds VALUES ('" + potID + "', 'soilMoisture', '" + \
                str(self.__defaultThresholdValue) + "', '" + self.__defaultLessGreaterThan + \
                "', '" + tdate + "', '" + ttime + "')"    
        self.insertDBData(mySQL)
        mySQL = "INSERT INTO userThresholds VALUES ('" + potID + "', 'roomTemperature', '" + \
                str(self.__defaultThresholdValue) + "', '" + self.__defaultLessGreaterThan + \
                "', '" + tdate + "', '" + ttime + "')"    
        self.insertDBData(mySQL)
        mySQL = "INSERT INTO userThresholds VALUES ('" + potID + "', 'roomHumidity', '" + \
                str(self.__defaultThresholdValue) +  "', '" + self.__defaultLessGreaterThan + \
                "', '" + tdate + "', '" + ttime + "')"    
        self.insertDBData(mySQL)
        if (self.__DEBUG):
            print("\nSet Default Thresholds")
        return
        
    #To blink a pin once
    def blink(self, pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        return
    
    #To insert data into the database
    def insertDBData(self, mySQL):
        #Try inserting data to database table
        try:
            #Insert data
            self.__cursor.execute(mySQL)
            self.__dbconnect.commit();
        except sqlite3.Error, e:
            #If error, blink db error LED
            if (self.__DEBUG):
                print ('\nDatabase Error %s:' % e.args[0])
            self.blink(self.__dberrorLED)
        return
        
    #To update user data in userPlantsTable
    def updateUserPlantsTable(self, userInfo):
        potID = str(userInfo.get('potID'))
        roomID = str(userInfo.get('roomID'))
        ownerID = str(userInfo.get('ownerID'))
        #Inserting user data into db
        mySQL = "INSERT INTO userPlants VALUES ('" + potID + "', '" + roomID + "', '" + ownerID + "')"    
        self.insertDBData(mySQL)
        if (self.__DEBUG):
            print("\nUpdated User Data")
        return
    
    #To update notes in userNotesTable
    def updateUserNotesTable(self, userNotes):
        potID = str(userNotes.get('potID'))
        notes = str(userNotes.get('notes'))
        tdate = str(date.today())
        ttime = str(datetime.now().strftime("%H:%M:%S"))
        #Inserting notes into db
        mySQL = "INSERT INTO userNotes VALUES ('" + potID + "', '" + notes + "', '" + tdate + "', '" + ttime + "')"
        self.insertDBData(mySQL)
        if (self.__DEBUG):
            print("\nUpdated Notes Data")
        return
    
    #To notifcations msgs to the app
    def notifyApp(self, message):
        #If ack received, try sending again for certain number of times
        i = 0
        while(i <= self.__numRetries):
            if (self.send_App_Msg(message) == True):
                #Ack has been received, return
                return
            i = i + 1
        #Stop trying to send msg
        return   
  
    #To send msgs to the app and wait for ack (times out if no ack received)
    def send_App_Msg(self, message):
        self.__soc_send.sendto(message, self.__app_addrs)
        if (self.__DEBUG):
            print("\nNotifcation has been sent to App: " + message)
        startTime = time.time()
        endTime = self.__ack_endTime
        self.__soc_recv.settimeout(self.__ack_timeout)
        while (True):
            #If less than a endTime amount of time
            if time.time() < (startTime + endTime):
                try:
                    #Try Receving otherwise timeout and retry
                    if (self.__DEBUG):
                        print("Waiting for Acknowledgement . . .")
                    buf, address = self.__soc_recv.recvfrom(self.__port)
                    #If buf is received, try to load it
                    buf = json.loads(buf)
                    if not len(buf):
                        #No ack received, retry
                        continue
                    else:
                        if (buf.get("opcode") == "0"):
                            #Ack recevied, blink ack led
                            if (self.__DEBUG):
                                print("Acknowledgement Received")
                            self.blink(self.__sendLED)
                            return True
                        else:
                            #No ack received, retry
                            continue
                except (ValueError, KeyError, TypeError):
                    #Ack not received, try again
                    continue
                except socket.timeout:
                    if (self.__DEBUG):
                        print("Receiving is Timed Out")
                    #Restart while loop (Retry)
                    continue
            else:
                #Failed to receive ack within a endTime amount of time
                return False
        return
    
    #To get requested stats from the db
    def get_stats(self, rowNumbers, sensors, potID):
        #Try retrieving data from the database
        try:
            #Retrieve Data
            #If potID doesn't exist, it returns an empty array without having any errors
            sensors = sensors.replace('"',"").replace("'","").replace('[',"").replace(']',"")
            mysql = """SELECT """ + sensors + """, tdate, ttime FROM (
            SELECT * FROM userPlants a
            INNER JOIN potData b
            ON a.potID = b.potID 
            INNER JOIN roomData c 
            ON a.roomID = c.roomID AND b.tdate = c.tdate AND b.ttime = c.ttime
            WHERE a.potID = """ + str(potID) + \
            """ ORDER BY c.tdate DESC, c.ttime DESC LIMIT """ + str(rowNumbers) + """)"""
            myresult = self.__cursor.execute(mysql).fetchall()
        except sqlite3.Error, e:
            #If error, blink db error led, return empty array
            if (self.__DEBUG):
                print '\nDatabase Error %s:' % e.args[0]
            self.blink(self.__dberrorLED)
            return "[]"
        #Convert data into json format
        stats = json.dumps( [dict(i) for i in myresult] )
        stats = stats.replace("temperature", "t").replace("light", "l").replace("humidity", "h").replace("soilMoisture", "s").replace("waterDistance", "w").replace("ttime", "T").replace("tdate", "d")
        if (self.__DEBUG):
            print("\nData Retreived from DB")
        return stats
    
    #To send the stats with the corresponding opcode
    def send_stats(self, rowNumbers, sensors, potID):
        if rowNumbers == 0:
            #0 means to send app just one most recent row of data (opcode E)
            oneRow = self.get_stats(1, sensors, potID)
            stats = '{"opcode" : "7", "statsArray" : ' + str(oneRow) + '}'
        else:
            #Otherwise send mutiple recent rows of data (opcode 6)
            manyRows = self.get_stats(rowNumbers, sensors, potID)
            stats = '{"opcode" : "6", "statsArray" : ' + str(manyRows) + '}'
        #Send stats to App
        self.notifyApp(stats)
        return


#Main function which receives json data and invokes methods based on opcode received
def main():
    DEBUG = True
    #Create GlobalServer object (port, room_ip_addrs, app_ip_addrs, DEBUG)
    globalServer = GlobalServerApp(8008,'192.168.137.102', DEBUG)
    while True:
        #receive
        data = GlobalServerApp.receive()
        if (data ==  None):
            #If length of buffer is <1, try receiving again
            continue
        else:
            message = data[0] #The loaded buffer version
            #User wants to update notes table
            if (message.get('opcode') == "1"):
                GlobalServerApp.updateUserNotesTable(message)
            #User wants to add a pot with a room and owner
            if (message.get('opcode') == "2"): 
                #Set default thresholds for that potID
                GlobalServerApp.setDefaultThresholds(str(message.get("potID")))
                #Update user plants table
                GlobalServerApp.updateUserPlantsTable(message)
            #If user wants to set thresholds to requested ones
            if (message.get('opcode') == "3"): 
                GlobalServerApp.updateUserThresholdsTable(message)
            #If user wants to view stats
            if (message.get('opcode') == "5"):
                rowNumbers = message.get("rowNumbers")
                sensors = message.get("sensorType")
                potID = message.get("potID")
                GlobalServerApp.send_stats(rowNumbers, sensors, potID)      
    self.__soc_recv.shutdown(1)
    self.__soc_send.shutdown(1)
    self.__cursor.close()
    return
    
if __name__== "__main__":
    main()



