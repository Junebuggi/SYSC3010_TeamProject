#Author: Abeer Rafiq
#Modified: 10/24/2019
#Source: https://pymotw.com/2/socket/udp.html
#Source: https://www.tutorialspoint.com/python/python_database_access.htm

#Importing Packages
import socket, sys, time, json
import RPi.GPIO as GPIO
import sqlite3
from datetime import datetime, date

    
def receiver():
    global buf, s_receive
    buf, address = s_receive.recvfrom(1000)
    
    GPIO.output(15, True)  
    time.sleep(1)  
    GPIO.output(15, False)  
    time.sleep(1)
        
    return buf

def sender(jsonstr, addrs_send):
    print("SENDING: " + jsonstr + ", TO: " + str(addrs_send))
    s_send.sendto(jsonstr, addrs_send)
    return
    
def testReceiveAck(buf):
    if(buf == "ack"):
        print("RECEIVED: " + buf)
        return
    else:
        #notifyUser("00000000001")
        return

def setGlobalServer():
    #Initializing GPIO
    global GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(15, GPIO.OUT) #green LED - receiving data properly
    GPIO.setup(18, GPIO.OUT) #blue LED - error in receiving data
 
    global s_receive, s_send, server_addrs_receive, room_addrs_send
    #Intializing and setting sockets and ports
    s_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addrs_receive = ('', 1000)
    s_receive.bind(server_addrs_receive)

    s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    room_addrs_send = ('169.254.14.50', 1000)
    
    global cursor, dbconnect
    #Connecting to the database
    dbconnect = sqlite3.connect("/home/pi/Documents/Team_Project/dataBases/plantNurseryDB.db");
    dbconnect.row_factory = sqlite3.Row;
    cursor = dbconnect.cursor();
    return

def setPlantNurseryApp():
    global app_s_send, app_addrs_send
    
    app_s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    app_addrs_send = ('172.17.63.157', 1000)
    return
 
    
def updateUserNotesTable(userNotes):
    global cursor, dbconnect
    
    potID = userNotes.get('potID')
    roomID = userNotes.get('roomID')
    notes = userNotes.get('notes')
    tdate = str(date.today()) 
    ttime = str(datetime.now().strftime("%H:%M:%S"))     
    
    mySQL = "insert into userNotes values ('" + str(potID) "', '" + str(roomID) + "', '" + str(notes) + "', '" + str(tdate) + "', '" + str(ttime) + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
    return

def sendSocketAck(address)
    sender('{"opcode" : "0"}', address)
    return

def updateUserThresholdsTable(threshold):
    global cursor, dbconnect
    global lightThreshold, soilMoistureThreshold, roomHumidityThreshold, roomTemperatureThreshold
    global lightLessGreaterThan, soilMoistureLessGreaterThan, roomHumidityLessGreaterThan, roomTemperatureLessGreaterThan
    
    potID = threshold.get("potID")
    lessGreaterThan = threshold.get("lessGreaterThan")
    thresholdValue = threshold.get("thresholdValue")
    sensorType = threshold.get("sensorType")
    tdate = str(date.today()) 
    ttime = str(datetime.now().strftime("%H:%M:%S")) 
    
    mySQL = "insert into userThresholds values ('" + str(potID) "', '" + str(roomID) + "', '" + str(sensorType) + "', '" + str(thresholdValue) + "', '" + str(lessGreaterThan) + "', '" + str(tdate) + "', '" + str(ttime) + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
    
    if sensorType == "light":
        lightThreshold = float(thresholdValue)
        lightLessGreaterThan = lessGreaterThan
    elif sensorType == "soilMoisture":
        soilMoistureThreshold = float(thresholdValue)  
        soilMoistureLessGreaterThan = lessGreaterThan
    elif sensorType == "roomTemperature":
        roomHumidityThreshold = float(thresholdValue)
        roomHumidityLessGreaterThan = lessGreaterThan
    elif sensorType == "roomHumidity":
        roomTemperatureThreshold = float(thresholdValue)
        roomTemperatureLessGreaterThan = lessGreaterThan
    return


def getStats(request):
    global cursor
    rownumbers = request.get("rowNumbers")
    sensorType = request.get("sensorType")
    sensorType = sensorType.replace('"',"").replace("'","").replace('[',"").replace(']',"")

    if (sensorType != "temperature") | (sensorType != "humidity") | (sensorType != "DHT22Status"):
        tableName = "potData"
    else:
        tableName = "roomData"

    cursor.execute('SELECT ' + sensorType + ', tdate, ttime FROM ' + tableName + ' ORDER BY tdate DESC, ttime DESC LIMIT ' + rownumbers)
    data = cursor.fetchall()
    
    jsonstr = '{"opcode" : "6", '
    j = 1
    string = "("
    for row in data:
        for i in range(len(row)-1):
            string = string + str(row[i]) + ", "
        string = string + str(row[len(row)-1]) + ")"
        jsonstr = jsonstr + '"' + str(j) + '" : "' + string + '", '
        j = j+1
        string = "("
    jsonstr = jsonstr[:len(jsonstr) -2] + '}'
    
    return statsStr

def sendStats(statsStr):
    global app_addrs_send
    sender(statsStr, app_addrs_send)
    return

def updateUserPlantsTable(userInfo):
    global cursor, dbconnect

    if roomID in userInfo:
        roomID = userInfo.get('roomID')
    else:
        roomID = ""
        
    if roomName in userInfo:
        roomName = userInfo.get('roomName')
    else:
        roomName = ""
        
    if potID in userInfo:
        potID = userInfo.get('potID')
    else:
        potID = ""
    
    if plantName in userInfo:
        plantName = userInfo.get('plantName')
    else:
        plantName = ""
    
    if owner in userInfo:
        owner = userInfo.get('owner')
    else:
        owner = ""
        
    mySQL = "insert into userPlants values ('" + str(potID) + "', '" + str(plantName) + "', '" + str(roomID) + "', '" + str(roomName) + "', '" + str(owner) + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
    return

def getUserThresholds():
    global cursor
    global lightThreshold, soilMoistureThreshold, roomHumidityThreshold, roomTemperatureThreshold
    global lightLessGreaterThan, soilMoistureLessGreaterThan, roomHumidityLessGreaterThan, roomTemperatureLessGreaterThan
    
    cursor.execute("SELECT EXISTS(SELECT 1 FROM userThresholds WHERE sensorType='light' LIMIT 1)")
    record = cursor.fetchone()
    if record[0] != 1:
        setThreshold({"sensorType" : "light", "thresholdValue" : "80", "lessGreaterThan" : ">"})
    cursor.execute("SELECT EXISTS(SELECT 1 FROM userThresholds WHERE sensorType='soilMoisture' LIMIT 1)")
    record = cursor.fetchone()
    if record[0] != 1:
        setThreshold({"sensorType" : "soilMoisture", "thresholdValue" : "80", "lessGreaterThan" : ">"})
    cursor.execute("SELECT EXISTS(SELECT 1 FROM userThresholds WHERE sensorType='roomTemperature' LIMIT 1)")
    record = cursor.fetchone()
    if record[0] != 1:
        setThreshold({"sensorType" : "roomTemperature", "thresholdValue" : "80", "lessGreaterThan" : ">"})
    cursor.execute("SELECT EXISTS(SELECT 1 FROM userThresholds WHERE sensorType='roomHumidity' LIMIT 1)")
    record = cursor.fetchone()
    if record[0] != 1:
        setThreshold({"sensorType" : "roomHumidity", "thresholdValue" : "80", "lessGreaterThan" : ">"})
        
    cursor.execute('SELECT sensorType, thresholdValue, lessGreaterThan, tdate, ttime FROM userThresholds ORDER BY tdate DESC, ttime DESC LIMIT 4')
    data = cursor.fetchall()
    for row in data:
        if row[0] == 'light':
            lightThreshold = row[1]
            lightLessGreaterThan = row[2]
        if row[0] == 'soilMoisture':
            soilMoistureThreshold = row[1]
            soilMoistureLessGreaterThan = row [2]
        if row[0] == 'roomHumidity':
            roomHumidityThreshold = row[1]
            roomHumidityLessGreaterThan = row[2]
        if row[0] == 'roomTemperature':
            roomTemperatureThreshold = row[1]
            roomTemperatureLessGreaterThan= row[2]
    return

def checkUserThresholds():
    global lightThreshold, soilMoistureThreshold, roomHumidityThreshold, roomTemperatureThreshold
    global lightLessGreaterThan, soilMoistureLessGreaterThan, roomHumidityLessGreaterThan, roomTemperatureLessGreaterThan
    global light, soilMoisture, temperature, humidity
    
    if lightLessGreaterThan == ">":
        if light > lightThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0"}')
    elif lightLessGreaterThan == "<":
        if light < lightThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0"}')
    if roomHumidityLessGreaterThan == ">":
        if humidity > roomHumidityThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0"}')
    elif roomHumidityLessGreaterThan == "<":
        if humidity < roomHumidityThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0"}')            
    if roomTemperatureLessGreaterThan == ">":
        if temperature > roomTemperatureThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0"}')
    elif roomTemperatureLessGreaterThan == "<":
        if temperature < roomTemperatureThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0"}')
    if soilMoistureLessGreaterThan == ">":
        if soilMoisture > soilMoistureThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0"}')
            cursor.execute('SELECT waterPumpDuration, tdate, ttime FROM userThresholds ORDER BY tdate DESC, ttime DESC LIMIT 1')
            data = cursor.fetchall()
            waterPumpDuration = data[0][1]
            startPumpStr = '{"opcode" : "4", "pumpDuration" : "' + waterPumpDuration + '"}'
            startWaterPump(startPumpStr) #sends to room pi receives ack
            notifyUser(startPumpStr) #receives ack
    elif soilMoistureLessGreaterThan == "<":
        if soilMoisture < soilMoistureThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0"}')

    return

def updateRoomTable(sensorInfo):
    global cursor, dbconnect, temperature, humidity 
    
    temperature = ("{0:.2f}".format(sensorInfo.get('temperature')))
    humidity = ("{0:.2f}".format(sensorInfo.get('humidity')))
    tdate = sensorInfo.get('tdate')
    ttime = sensorInfo.get('ttime')
    roomID = sensorInfo.get('roomID')
    DHT22Status = sensorInfo.get('DHT22Status')
    
    mySQL = "insert into roomData values ('" + str(roomID) + "', '" + str(temperature) + "', '" + str(humidity) + "', '" + str(DHT22Status) + "' , '" + tdate + "', '" + ttime + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
    return

def updatePotTable(sensorInfo):
    global cursor, dbconnect, light, soilMoisture
    
    potID = sensorInfo.get('potID')
    waterDistance = sensorInfo.get('waterDistance')
    waterDistanceStatus = sensorInfo.get('waterDistanceStatus')
    light = sensorInfo.get('light')
    ldrStatus = sensorInfo.get('ldrStatus')
    soilMoisture = sensorInfo.get('soilMoisture')
    soilMoistureStatus = sensorInfo.get('soilMoistureStatus')
    waterPumpStatus = sensorInfo.get('waterPumpStatus')
    tdate = sensorInfo.get('tdate')
    ttime = sensorInfo.get('ttime')
    
    mySQL = "insert into potData values ('" + str(potID) + "', '" + str(light) + "', '" + str(soilMoisture) + "', '" + str(waterDistance) + "', '" + str(ldrStatus) + "', '" + str(waterPumpStatus) + "', '" + str(waterDistanceStatus) + "', '" + str(waterMoistureStatus) + "', '" + tdate + "', '" + ttime + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
    return


def notifyUser(message):
    global app_addrs_send
    sender(message, app_addrs_send)
    testReceiveAck(receiver()) #receives ack
    return


def startWaterPump(startPump):
    global room_addrs_send
    sender(startPump, room_addrs_send)
    testReceiveAck(receiver())
    return

setGlobalServer()
setPlantNurseryApp()
getUserThresholds()

while True:
    message = receiver()
    message = json.loads(message)
    if (message.get('opcode') == "1"): #update userNotesTable
        sendSocketAck(app_addrs_send)
        updateUserNotesTable(message)
    if (message.get('opcode') == "3"): #setting thresholds
        sendSocketAck(app_addrs_send)
        updateUserThresholdsTable(message)
    if (message.get('opcode') == "5"): #05 view stats
        sendSocketAck(app_addrs_send) #send ack
        sendStats(getStats(message)) #gets db stats and sends to app 
        testReceiveAck(receiver()) #receives ack from app
    if (message.get('opcode') == "7"): #set up room
        updateUserPlantTable(message)
    if (message.get('opcode') == "2"): # set up pot
        updateUserPlantTable(message)
    if (message.get("opcode") == "D");
        sendSocketAck(room_addrs_send) #send ack
        notifyUser(str(message)) #notify app and wait for ack    
    if (message.get('opcode') == "9"): #all data
        sendSocketAck(room_addrs_send) #send ack
        checkUserThresholds() #check and notify user if not met
        updateRoomTable(message) #update table
        updatePotTable(message) #update table
    if (message.get('opcode') == "A"):
        sendSocketAck(room_addrs_send)
        notifyUser(message)

#Shutdown Socket
s.shutdown(1)
#Close Database
db.close()

#GLOBAL SERVER