#Author: Abeer Rafiq
#Modified: 11/20/2019
#Source: https://pymotw.com/2/socket/udp.html
#Source: https://www.tutorialspoint.com/python/python_database_access.htm

#Importing Packages
import socket, sys, time, json
import RPi.GPIO as GPIO
import sqlite3
from datetime import datetime, date

def receiver():
    global buf, s_receive, port
   
    print("Receiving")
    buf, address = s_receive.recvfrom(port)
    print("Received", buf)
    return buf


def setGlobalServer():
    global s_receive, s_send, server_addrs_receive, room_addrs_send, port
    global cursor, dbconnect
   
    port = 8008
    room_ip_address = '192.168.137.103'
   
    s_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addrs_receive = ('', port)
    s_receive.bind(server_addrs_receive)

    s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    room_addrs_send = (room_ip_address, port)
   
    dbconnect = sqlite3.connect("/home/pi/Documents/Team_Project/dataBases/plantNurseryDB.db");
    dbconnect.row_factory = sqlite3.Row;
    cursor = dbconnect.cursor();
    return

def setPlantNurseryApp():
    global app_s_send, app_addrs_send, port
   
    app_ip_address = '192.168.137.102'
    app_s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    app_addrs_send = (app_ip_address, port)
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
   
    mySQL = "insert into userThresholds values ('" + str(potID) + "', '" + str(sensorType) + "', '" + str(thresholdValue) + "', '" + str(lessGreaterThan) + "', '" + str(tdate) + "', '" + str(ttime) + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
   
    if sensorType == "light":
        lightThreshold = float(str(thresholdValue))
        lightLessGreaterThan = str(lessGreaterThan)
    elif sensorType == "soilMoisture":
        soilMoistureThreshold = float(str(thresholdValue))  
        soilMoistureLessGreaterThan = str(lessGreaterThan)
    elif sensorType == "roomTemperature":
        roomHumidityThreshold = float(str(thresholdValue))
        roomHumidityLessGreaterThan = str(lessGreaterThan)
    elif sensorType == "roomHumidity":
        roomTemperatureThreshold = float(str(thresholdValue))
        roomTemperatureLessGreaterThan = str(lessGreaterThan)
    return

def updateUserPlantsTable(userInfo):
    global cursor, dbconnect


    potID = userInfo.get('potID')
    roomID = userInfo.get('roomID')
    ownerID = userInfo.get('ownerID')
    print(potID)
   
    mySQL = "insert into userPlants values ('" + str(potID) + "', '" + str(roomID) + "', '" + str(ownerID) + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
    return

 
def updateUserNotesTable(userNotes):
    global cursor, dbconnect
   
    potID = userNotes.get('potID')
    notes = userNotes.get('notes')
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))    
   
    mySQL = "insert into userNotes values ('" + str(potID) + "', '" + str(notes) + "', '" + str(tdate) + "', '" + str(ttime) + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
    return  

def updatePotTable(sensorInfo):
    global cursor, dbconnect, light, soilMoisture
   
    potID = sensorInfo.get('potID')
    waterDistance = sensorInfo.get('waterDistance')
    light = sensorInfo.get('light')
    ldrStatus = sensorInfo.get('ldrStatus')
    soilMoisture = sensorInfo.get('soilMoisture')
    soilMoistureStatus = sensorInfo.get('soilMoistureStatus')
    waterPumpStatus = sensorInfo.get('waterPumpStatus')
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    mySQL = "insert into potData values ('" + str(potID) + "', '" + str(light) + "', '" + str(soilMoisture) + "', '" + str(waterDistance) + "', '" + tdate + "', '" + ttime + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
    return

def updateRoomTable(sensorInfo):
    global cursor, dbconnect, temperature, humidity
   
    temperature = ("{0:.2f}".format(sensorInfo.get('temperature')))
    humidity = ("{0:.2f}".format(sensorInfo.get('humidity')))
    tdate = sensorInfo.get('tdate')
    ttime = sensorInfo.get('ttime')
    roomID = sensorInfo.get('roomID')
    DHT22Status = sensorInfo.get('DHT22Status')
   
    mySQL = "insert into roomData values ('" + str(roomID) + "', '" + str(temperature) + "', '" + str(humidity) + "' , '" + tdate + "', '" + ttime + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
    return


def setUserThresholds(potID):
    global cursor
    global lightThreshold, soilMoistureThreshold, roomHumidityThreshold, roomTemperatureThreshold
    global lightLessGreaterThan, soilMoistureLessGreaterThan, roomHumidityLessGreaterThan, roomTemperatureLessGreaterThan
   
    updateUserThresholdsTable({"potID" : potID, "sensorType" : "light", "thresholdValue" : "80", "lessGreaterThan" : ">"})
    updateUserThresholdsTable({"potID" : potID, "sensorType" : "soilMoisture", "thresholdValue" : "80", "lessGreaterThan" : ">"})
    updateUserThresholdsTable({"potID" : potID, "sensorType" : "roomTemperature", "thresholdValue" : "80", "lessGreaterThan" : ">"})
    updateUserThresholdsTable({"potID" : potID, "sensorType" : "roomHumidity", "thresholdValue" : "80", "lessGreaterThan" : ">"})
   
    defaultThresholdValue = "80"
    defaultLessGreaterThan = "<"
 
    lightThreshold = defaultThresholdValue
    lightLessGreaterThan = defaultLessGreaterThan
    soilMoistureThreshold = defaultThresholdValue
    soilMoistureLessGreaterThan = defaultLessGreaterThan
    roomHumidityThreshold = defaultThresholdValue
    roomHumidityLessGreaterThan = defaultLessGreaterThan
    roomTemperatureThreshold = defaultThresholdValue
    roomTemperatureLessGreaterThan= defaultLessGreaterThan
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
   
    mySQL = "insert into userThresholds values ('" + str(potID) + "', '" + str(sensorType) + "', '" + str(thresholdValue) + "', '" + str(lessGreaterThan) + "', '" + str(tdate) + "', '" + str(ttime) + "')"    
    cursor.execute(mySQL)
    dbconnect.commit();
   
    if sensorType == "light":
        lightThreshold = str(thresholdValue)
        lightLessGreaterThan = lessGreaterThan
    elif sensorType == "soilMoisture":
        soilMoistureThreshold = str(thresholdValue)  
        soilMoistureLessGreaterThan = lessGreaterThan
    elif sensorType == "roomTemperature":
        roomHumidityThreshold = str(thresholdValue)
        roomHumidityLessGreaterThan = lessGreaterThan
    elif sensorType == "roomHumidity":
        roomTemperatureThreshold = str(thresholdValue)
        roomTemperatureLessGreaterThan = lessGreaterThan
    return


def checkUserThresholds():
    global lightThreshold, soilMoistureThreshold, roomHumidityThreshold, roomTemperatureThreshold
    global lightLessGreaterThan, soilMoistureLessGreaterThan, roomHumidityLessGreaterThan, roomTemperatureLessGreaterThan
    global light, soilMoisture, temperature, humidity
   
    if lightLessGreaterThan == ">":
        if light > lightThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "1, 0, 0, 0, 0, 0, 0, 0, 0, 0"}')
    elif lightLessGreaterThan == "<":
        if light < lightThreshold:
            print("ENTERED")
            notifyUser('{"opcode" : "D", "sensorArray" : "1, 0, 0, 0, 0, 0, 0, 0, 0, 0"}')
    if roomHumidityLessGreaterThan == ">":
        if humidity > roomHumidityThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 1, 0, 0, 0, 0, 0, 0, 0, 0"}')
    elif roomHumidityLessGreaterThan == "<":
        if humidity < roomHumidityThreshold:
            print("ENTERED")
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 1, 0, 0, 0, 0, 0, 0, 0, 0"}')            
    if roomTemperatureLessGreaterThan == ">":
        if temperature > roomTemperatureThreshold:
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 0, 1, 0, 0, 0, 0, 0, 0, 0"}')
    elif roomTemperatureLessGreaterThan == "<":
        if temperature < roomTemperatureThreshold:
            print("ENTERED")
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 0, 1, 0, 0, 0, 0, 0, 0, 0"}')
    if soilMoistureLessGreaterThan == ">":
        if soilMoisture > soilMoistureThreshold:
            print("entered")
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 0, 0, 1, 0, 0, 0, 0, 0, 0"}')
            waterPumpDuration = 2
            startPumpStr = '{"opcode" : "4", "pumpDuration" : "' + waterPumpDuration + '"}'
            startWaterPump(startPumpStr) #sends to room pi receives ack
            notifyUser(startPumpStr) #receives ack
    elif soilMoistureLessGreaterThan == "<":
        if soilMoisture < soilMoistureThreshold:
            print("entered")
            notifyUser('{"opcode" : "D", "sensorArray" : "0, 0, 0, 1, 0, 0, 0, 0, 0, 0"}')
            waterPumpDuration = 10
            startPumpStr = '{"opcode" : "4", "pumpDuration" : "' + str(waterPumpDuration) + '"}'
            startWaterPump(startPumpStr) #sends to room pi receives ack
            notifyUser(startPumpStr) #receives ack
    return

def startWaterPump(startPump):
    global s_send, room_addrs_send
    print(startPump + " TO: " + str(room_addrs_send))
    s_send.sendto(startPump, room_addrs_send)
    return

def notifyUser(message):
    global app_addrs_send, app_s_send
    app_s_send.sendto(message, app_addrs_send)
    return

setGlobalServer()
setPlantNurseryApp()

while True:
    message = receiver()
    message = json.loads(message)
 
    if (message.get('opcode') == "1"): #update userNotesTable
        updateUserNotesTable(message)
    if (message.get('opcode') == "2"): # set up pot
        updateUserPlantsTable(message)
        setUserThresholds(message.get("potID"))
    if (message.get('opcode') == "3"): #setting thresholds
        updateUserThresholdsTable(message)
    if (message.get('opcode') == "D"): #setting thresholds
        notifyUser(message)
    if (message.get('opcode') == "9"): #all data
        print(message)
        #sendSocketAck(room_addrs_send) #send ack
        updateRoomTable(message) #update table
        updatePotTable(message) #update table
        checkUserThresholds() #check and notify user if not met
