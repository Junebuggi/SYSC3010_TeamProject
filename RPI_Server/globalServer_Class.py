#Author: Abeer Rafiq
#Modified: 11/23/2019 3:00pm

#Importing Packages
import socket, sys, time, json, sqlite3
import RPi.GPIO as GPIO
from datetime import datetime, date

#Creating a global server class
class GlobalServer:
    #The constructor
    def __init__(self, port, room_ip_addrs,
                 app_ip_addrs):
        #Setting port
        self.__port = int(port)
        #Setting socket to receive
        self.__soc_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_address = ('', self.__port)
        self.__soc_recv.bind(recv_address)
        #Setting socket/addresses to send to the room rpi and app
        self.__soc_send =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__room_addrs = (room_ip_addrs, self.__port)
        self.__app_addrs = (app_ip_addrs, self.__port)
        #Setting up led blinking
        self.__receiveLED = 14
        self.__sendLED = 15
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__receiveLED, GPIO.OUT)
        GPIO.setup(self.__sendLED, GPIO.OUT)
        #Setting up string for acknowldegements
        self.__ackstr = "{'opcode':'0'}"
        #Setting database connections
        dbpath = '/home/pi/Documents/Team_Project/dataBases/plantNursery_DB.db'
        self.__dbconnect = sqlite3.connect(dbpath); 
        self.__dbconnect.row_factory = sqlite3.Row;
        self.__cursor = self.__dbconnect.cursor()        
        #Setting up default threshold variables
        self.__defaultThresholdValue = 80
        self.__defaultLessGreaterThan = "<"
        self.__lightThreshold = self.__defaultThresholdValue
        self.__lightLessGreaterThan =  self.__defaultLessGreaterThan
        self.__soilMoistureThreshold = self.__defaultThresholdValue
        self.__soilMoistureLessGreaterThan =  self.__defaultLessGreaterThan
        self.__roomHumidityThreshold = self.__defaultThresholdValue
        self.__roomHumidityLessGreaterThan =  self.__defaultLessGreaterThan
        self.__roomTemperatureThreshold = self.__defaultThresholdValue
        self.__roomTemperatureLessGreaterThan =  self.__defaultLessGreaterThan
        self.__currentLight = 0
        self.__currentSoilMoisture = 0
        self.__currentWaterDistance = 0
        self.__currentRoomHumidity = 0
        self.__currentRoomTemperature = 0
        self.__waterPumpDuration = 2
        #Setting timeout/end time values
        self.__ack_timeout = 1
        self.__ack_endTime = 4
        print("\nGlobal Server Initialized")
    
    #To blink a pin once
    def blink(self, pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        return
    
    #Receives/returns buffer and sends ack 
    def receive(self):
        #Receiving
        print("\nWaiting to receive on port %d ... " % self.__port)
        buf, address = self.__soc_recv.recvfrom(self.__port)
        if(len(buf) > 0):
            #Blink receive Led
            self.blink(self.__receiveLED)
            print ("Received %s bytes from '%s': %s " % (len(buf), address[0], buf))
            #Sending ack
            self.__soc_send.sendto(self.__ackstr, (address[0], self.__port))
            #Blink send Led
            self.blink(self.__sendLED)
            print ("Sent %s to %s" % (self.__ackstr, (address[0], self.__port)))
            #Give time for the ack sent to be acknowledged
            time.sleep(self.__ack_endTime)
            return buf
        else:
            return False
    
    #To insert data into the database
    def insertDBData(self, mySQL):
        #Try inserting data to database table
        try:
            #Insert data
            self.__cursor.execute(mySQL)
            self.__dbconnect.commit();
        except sqlite3.Error, e:
            #If error, exit program 
            print ('\nDatabase Error %s:' % e.args[0])
            self.__soc_recv.shutdown(1)
            self.__soc_send.shutdown(1)
            self.__cursor.close()
            sys.exit(1)
        return
        
    #To add default threshold entries into the db
    def setDefaultThresholds(self, potID):
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
        print("\nSet Default Thresholds")
        return
        
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
        print("\nSet User Requested Thresholds")
        return

    #To update user data in userPlantsTable
    def updateUserPlantsTable(self, userInfo):
        potID = str(userInfo.get('potID'))
        roomID = str(userInfo.get('roomID'))
        ownerID = str(userInfo.get('ownerID'))
        #Inserting user data into db
        mySQL = "INSERT INTO userPlants VALUES ('" + potID + "', '" + roomID + "', '" + ownerID + "')"    
        self.insertDBData(mySQL)
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
        print("\nUpdated Notes Data")
        return
    
    #To update pot data in db
    def updatePotTable(self, sensorInfo, tdate, time):
        potID = sensorInfo.get('potID')
        self.__currentWaterDistance = sensorInfo.get('waterDistance')
        self.__currentLight = sensorInfo.get('light')
        self.__currentSoilMoisture = sensorInfo.get('soilMoisture')
        #Inserting pot data into db
        mySQL = "INSERT INTO potData VALUES ('" + str(potID) + "', '" + str(self.__currentLight)+ "', '" + \
                str(self.__currentSoilMoisture) + "', '" + str(self.__currentWaterDistance) + "', '" + \
                tdate + "', '" + ttime + "')"    
        self.insertDBData(mySQL)
        print("\nUpdated Pot Data")
        return
    
    #To update room data in db
    def updateRoomTable(self, sensorInfo,tdate, time):
        self.__currentRoomTemperature = round(sensorInfo.get('temperature'), 2)
        self.__currentRoomHumidity = round(sensorInfo.get('humidity'), 2)
        roomID = sensorInfo.get('roomID')
        #Inserting room data into db
        mySQL = "insert into roomData values ('" + str(roomID) + "', '" + str(self.__currentRoomTemperature) + \
                "', '" + str(self.__currentRoomHumidity) + "' , '" + tdate + "', '" + ttime + "')"    
        self.insertDBData(mySQL)
        print("\nUpdated Room Data")
        return


    #To compare current sensor data to threshold values
    def checkUserThresholds(self):
        #Notification json         #Should be receiving an ack so timeout if no ack receivedstrings
        lightNotfn = '{"opcode" : "D", "sensorArray" : "1, 0, 0, 0, 0, 0, 0, 0, 0, 0"}'        
        roomHumidityNotfn = '{"opcode" : "D", "sensorArray" : "0, 1, 0, 0, 0, 0, 0, 0, 0, 0"}'
        roomTemperatureNotfn = '{"opcode" : "D", "sensorArray" : "0, 0, 1, 0, 0, 0, 0, 0, 0, 0"}'
        soilMoistureNotfn = '{"opcode" : "D", "sensorArray" : "0, 0, 0, 1, 0, 0, 0, 0, 0, 0"}'
        #Tuples of sensor data to easily neatly
        light = (self.__currentLight, self.__lightThreshold, self.__lightLessGreaterThan, lightNotfn)
        soilMoisture = (self.__currentSoilMoisture, self.__soilMoistureThreshold, \
                        self.__soilMoistureLessGreaterThan, soilMoistureNotfn, self.__waterPumpDuration)
        roomHumidity = (self.__currentRoomHumidity, self.__roomHumidityThreshold, \
                        self.__roomHumidityLessGreaterThan, roomHumidityNotfn)
        roomTemperature = (self.__currentRoomTemperature, self.__roomTemperatureThreshold, \
                            self.__roomTemperatureLessGreaterThan, roomTemperatureNotfn)
        #Combined tuples for sensors
        sensorArr = [light, roomHumidity, roomTemperature, soilMoisture]
        #For each sensor compare current sensor value with threshold value
        for sensor in sensorArr:
            if sensor[2] == ">":
                if sensor[0] > sensor[1]:
                    #Threshold is met, notify user
                    notifyApp(sensor[3])
                    if(len(sensor) == 4):
                        #Soil moisture's threshold is met, then start water pump, notify user
                        startPumpStr = '{"opcode" : "4", "pumpDuration" : "' + str(sensor[4]) + '"}'
                        startWaterPump(startPumpStr) 
                        notifyApp(startPumpStr) 
            elif sensor[2] == "<":
                if sensor[0] < sensor[1]:
                    #Threshold is met, notify user
                    notifyApp(sensor[3])
                    if(length(sensor) == 4):
                        #Soil moisture's threshold is met, then start water pump, notify user
                        startPumpStr = '{"opcode" : "4", "pumpDuration" : "' + str(sensor[4]) + '"}'
                        startWaterPump(startPumpStr) 
                        notifyApp(startPumpStr) 
        print("\Thresholds Compared")
        return
    
    #Send room rpi msg to start water pump
    def startWaterPump(self, startPump):
        if (self.send_Room_Msg(startPump) == False):
            #If no ack received, send msg again
            print("\nStart Water Pump sent again to server")
            self.startWaterPump(startPump)
        return
    
    #To send msgs to the room and wait for ack
    def send_Room_Msg(self, message):
        self.__soc_send.sendto(message, self.__room_addrs)
        #Blink send LED
        self.blink(self.__sendLED)
        print("\Message sent to Room: " + message)
        #Should be receiving an ack so timeout if no ack received
        soc_recv.settimeout(self.__ack_timeout)
        startTime = time.time()
        endTime = self.__ack_endTime
        while (True):
            #If less than a endTime amount of time
            if time.time() < (startTime + endTime):
                try:
                    #Try Receving otherwise timeout and retry
                    print("Waiting for Acknowledgement . . .")
                    buf, address = soc_recv.recvfrom(self.__port)
                except socket.timeout:
                    print("Receiving is Timed Out")
                    #Restart while loop (Retry)
                    continue
                try:
                    #If buf is received, try to load it
                    buf = json.loads(buf)
                    if not len(buf):
                        #No ack received, retry
                        continue
                    else:
                        if (buf.get("opcode") == "0"):
                            #Ack recevied!
                            print("Acknowledgement Received")
                            return True
                        else:
                            #No ack received, retry
                            continue
                except (ValueError, KeyError, TypeError):
                    #Ack not received, try again
                    continue
            else:
                #Failed to receive ack within a endTime amount of time
                return False
        return
    
    #To notifcations msgs to the app
    def notifyApp(self, message):
        if (self.send_App_Msg(message) == False):
            #If no ack received, send msg again
            print("\nNotification sent again to server")
            self.notifyApp(message)
        return
    
    #To send msgs to the app and wait for ack
    def send_App_Msg(self, message):
        self.__soc_send.sendto(message, self.__app_addrs)
        #Blink send LED
        self.blink(self.__sendLED)
        print("\nNotifcation sent to App: " + message)
        #Should be receiving an ack so timeout if no ack received
        soc_recv.settimeout(self.__ack_timeout)
        startTime = time.time()
        endTime = self.__ack_endTime
        while (True):
            #If less than a endTime amount of time
            if time.time() < (startTime + endTime):
                try:
                    #Try Receving otherwise timeout and retry
                    print("Waiting for Acknowledgement . . .")
                    buf, address = soc_recv.recvfrom(self.__port)
                except socket.timeout:
                    print("Receiving is Timed Out")
                    #Restart while loop (Retry)
                    continue
                try:
                    #If buf is received, try to load it
                    buf = json.loads(buf)
                    if not len(buf):
                        #No ack received, retry
                        continue
                    else:
                        if (buf.get("opcode") == "0"):
                            #Ack recevied!
                            print("Acknowledgement Received")
                            return True
                        else:
                            #No ack received, retry
                            continue
                except (ValueError, KeyError, TypeError):
                    #Ack not received, try again
                    continue
            else:
                #Failed to receive ack within a endTime amount of time
                return False
        return
    
    #To get requested stats from the db
    def get_stats(self, rowNumbers, sensors):
        #Try retrieving data from the database
        try:
            #Retrieve Data
            sensors = sensors.replace('"',"").replace("'","").replace('[',"").replace(']',"")
            mysql = """SELECT """ + sensors + """, tdate, ttime FROM (
            SELECT * FROM userPlants a
            INNER JOIN potData b
            ON a.potID = b.potID 
            INNER JOIN roomData c 
            ON a.roomID = c.roomID AND b.tdate = c.tdate AND b.ttime = c.ttime
            ORDER BY c.tdate DESC, c.ttime DESC LIMIT """ + str(rowNumbers) + """)"""
            myresult = self.__cursor.execute(mysql).fetchall()
        except sqlite3.Error, e:
            #If error, exit program 
            print '\nDatabase Error %s:' % e.args[0]
            sys.exit(1)
        #Convert data into json format
        stats = json.dumps( [dict(i) for i in myresult] )
        print("\nData Retreived from DB")
        return stats
    
    #To send the stats with the corresponding opcode
    def send_stats(self, rowNumbers, sensors):
        if rowNumbers == '0':
            #0 means to send app just one most recent row of data (opcode E)
            oneRow = globalServer.get_stats(1, sensors)
            stats = '{"opcode" : "E", "statsArray" : "' + str(oneRow) + '"}'
        else:
            #Otherwise send mutiple recent rows of data (opcode 6)
            manyRows = globalServer.get_stats(rowNumbers, sensors)
            stats = '{"opcode" : "6", "statsArray" : "' + str(manyRows) + '"}'
        #Send stats to App
        #If ack received return
        if (self.send_notifyApp(error) == True):
            print("\nStats sent to app")
        else:
            #If no ack received, try sending again
            print("\nStats sent again to app (notify again)")
            self.send_stats(rowNumbers, sensors)
        return

#Main function which receives json data and invokes methods based on opcode received
def main():
    #Create GlobalServer object (port, room_ip_addrs, app_ip_addrs)
    globalServer = GlobalServer(1000, '192.168.1.47',
                              '192.168.137.102')
    while True:
        message = globalServer.receive()
        if (message ==  False):
            #If length of buffer is <1
            continue
        else:
            message = json.loads(message)
            #User wants to update notes table
            if (message.get('opcode') == "1"):
                globalServer.updateUserNotesTable(message)
            #User wants to add a pot with a room and owner
            if (message.get('opcode') == "2"): 
                globalServer.updateUserPlantsTable(message)
                #Set default thresholds for that potID
                globalServer.setDefaultThresholds(message.get("potID"))
            #If user wants to set thresholds to requested ones
            if (message.get('opcode') == "3"): 
                globalServer.updateUserThresholdsTable(message)
            #If user wants to view stats
            if (message.get('opcode') == "5"):
                rowNumbers = message.get("rowNumbers")
                sensors = message.get("sensorType")
                globalServer.send_stats(rowNumbers, sensors)
            #If an error has occured in the room rpi or arduino
            if (message.get('opcode') == "D"): 
                globalServer.notifyApp(str(message))
            #If room rpi sent all sensory data, update tables, compare values to thresholds as well
            if (message.get('opcode') == "9"): 
                tdate = str(date.today())
                ttime = str(datetime.now().strftime("%H:%M:%S"))
                globalServer.updateRoomTable(message, tdate, ttime)
                globalServer.updatePotTable(message, tdate, ttime) 
                globalServer.checkUserThresholds()        
    self.__soc_recv.shutdown(1)
    self.__soc_send.shutdown(1)
    self.__cursor.close()
    return
    
if __name__== "__main__":
    main()
