#Autho: Abeer Rafiq
#Modified: 10/24/2019
#Source: https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/
#Source: https://pymotw.com/2/socket/udp.html

#Importing Packages
import socket, sys, time, json
import RPi.GPIO as GPIO
import Adafruit_DHT
from datetime import datetime, date
import serial

global roomID
roomID = 0

def setRoomPi():
    #initializing GPIO
    global GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT) #Red LED to detect if measurements are read properly

    #Itnializing host, sockets and ports
    global s_receive, s_send, room_addrs_receive, server_addrs_send
    s_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addrs_send = ('169.254.171.154', 1000)
    
    s_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    room_addrs_receive = ('', 1000)
    s_receive.bind(room_addrs_receive)

    #IntializingTemperature and Humidity Sensor
    global DHT_SENSOR, DHT_PIN
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4
    
    global ser


    ser = serial.Serial('/dev/tty.usbmodem145101', 9600)
    ser.baudrate = 9600
    ser.flushInput()
    return

    



def startWaterPump(pumpDuration):
    if type(pumpDuration) is int and pumpDuration >= 1: 
        pumpMessage = "C," + pumpDuration + "\n"
        ser.write((pumpString).encode("utf-8")) 
    else:
        raise ValueError("Pump duration must be an integer AND must be greater than or equal to 1")
    return

def pumpFinished():
    stoppedPump = '{"opcode" : "A"}'
    sender(stoppedPump, server_addrs_send)
    testReceiveAck(receiver())
    return

def sender(jsonstr, addrs_send):
    print("SENDING: " + jsonstr + ", TO: " + str(addrs_send) + "\n")
    s_send.sendto(jsonstr, addrs_send)
    return
    
def receiver():
    global s_receive
    buf, address = s_receive.recvfrom(1000)
    return (buf)

def testReceiveAck(buf):
    if (buf.get("opcode") == "0"):
        print("ACKNOWLEGDED", buf)
        return
    else:
        errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1"}')
        return
        
def readSerial():
    global ser    
    message = ser.readline().decode().strip('\r\n').split(",")
    message = json.loads(message)
    return message

def getPotData(potData):
    global waterPumpStatus, potID, waterDistance, waterDistanceStatus, light, ldrStatus, soilMoisture, soilMoistureStatus
    potID = potData.get('potID')
    waterDistance = potData.get('waterDistance')
    waterDistanceStatus = potData.get('waterDistanceStatus')
    light = potData.get('light')
    ldrStatus = potData.get('ldrStatus')
    soilMoisture = potData.get('soilMoisture')
    soilMoistureStatus = potData.get('soilMoistureStatus')
    waterPumpStatus = potData.get('waterPumpStatus')
    return
    
def collectRoomData():
    global humidity, temperature, DHT_SENSOR, DHT_PIN
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN);
    return

def testRoomSensors():
    global DHT22Status, temperature, humidity
    if humidity is not None and temperature is not None:
        DHT22Status = 1
    else:
        #If no data was retrieved blink Red LED to represent an error 
        print("Failed to retrieve data from humidity sensor")
        errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0"}')
        GPIO.output(14, True)  
        time.sleep(1)  
        GPIO.output(14, False)  
        time.sleep(1)
        DHT22Status = 0
        temperature = 0
        humidity = 0
    return

def errorDetected(error):
    sender(error, server_addrs_send)
    testReceiveAck(receiver())
    return

def sendSensoryData():
    global roomID, temperature, humidity, s_send, server_addrs_send, DHT22Status
    global waterPumpStatus, potID, waterDistance, waterDistanceStatus, light, ldrStatus, soilMoisture, soilMoistureStatus
    tdate = '"' + str(date.today()) + '"'
    ttime = '"' + str(datetime.now().strftime("%H:%M:%S")) + '"'
    jsonstr = '{"opcode": "9", "roomID": ' + str(roomID) + ', "potID": ' + str(potID) + ', "tdate": ' + str(tdate) + ', "ttime": ' + str(ttime) + ', "temperature": ' + str(temperature) + ', "humidity": ' + str(humidity) + ', "DHT22Status": ' + str(DHT22Status) + ', "waterDistance": ' + str(waterDistance) + ', "waterDistanceStatus": ' + str(waterDistanceStatus) + ', "light": ' + str(light) + ', "ldrStatus": ' + str(ldrStatus) + ', "soilMoisture": ' + str(soilMoisture) + ', "soilMoistureStatus": ' + str(soilMoistureStatus) + ', "waterPumpStatus": ' + str(waterPumpStatus) + '}'
    sender(jsonstr, server_addrs_send)
    testReceiveAck(receiver()) # wait for ack
    return

def sendAck(address):
    sender('{"opcode" : "0"}')
    return

def requestPotData(): #Ask the arduino for the potData
    ser.write(("E,").encode("utf-8"))
    flag = True
    startTime = time.time()
    while flag and (time.time() < startTime + 2):
        potData = ser.readline()
        if (len(data) > 0):
            potData = potData.decode().strip('\r\n')
            flag = False
            ser.write(("0,").encode("utf-8"))
            return potData
        else:
            ser.write(("E,").encode("utf-8"))
    return #TODO return JSON with null values

setRoomPi()
#Repeat
while 1:
    message = readSerial()
    if message.get('opcode') == 'D':
        errorDetected(message) #send error to app and receive ack
    if message.get('opcode') == '8':
        getPotData(message) #puts data into variables
        collectRoomData() #collect room data and puts into variables
        testRoomSensors() #test room sensors for errors, if error send error to global (receive ack)
        sendSensoryData() #send the data to global and receive ack
    if (message.get('opcode') == "A") #stop water pump
        pumpFinished() #sends to room pi and waits for ack
    
    message = receiver()
    message = json.loads(message)
    if (message.get('opcode') == "4"): #2 startwaterpump
        sendAck(server_addrs_send) #to server
        startWaterPump() 


#Shutdown socket
s.shutdown(1)

#ROOMPI
