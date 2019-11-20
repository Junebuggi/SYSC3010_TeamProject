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
    server_addrs_send = ('192.168.137.101', 8008)
   
    s_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    room_addrs_receive = ('', 8008)
    s_receive.bind(room_addrs_receive)

    #IntializingTemperature and Humidity Sensor
    global DHT_SENSOR, DHT_PIN
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4
   
    global ser


    #ser = serial.Serial('/dev/tty.usbmodem145101', 9600)
    #ser.baudrate = 9600
    ser = serial.Serial('/dev/ttyACM0', timeout = 0.1)
    ser.flushInput()
    return

   
def sender(jsonstr, addrs_send):
    #print("SENDING: " + jsonstr + ", TO: " + str(addrs_send) + "\n")
    s_send.sendto(jsonstr, addrs_send)
    return

def sendSensoryData():
    global roomID, temperature, humidity, s_send, server_addrs_send, DHT22Status
    global waterPumpStatus, potID, waterDistance, waterDistanceStatus, light, ldrStatus, soilMoisture, soilMoistureStatus
    tdate = '"' + str(date.today()) + '"'
    ttime = '"' + str(datetime.now().strftime("%H:%M:%S")) + '"'
    jsonstr = '{"opcode": "9", "roomID": ' + str(roomID) + ', "potID": ' + str(potID) + ', "tdate": ' + str(tdate) + ', "ttime": ' + str(ttime) + ', "temperature": ' + str(temperature) + ', "humidity": ' + str(humidity) + ', "waterDistance": ' + str(waterDistance) + ', "waterDistanceStatus": ' + str(waterDistanceStatus) + ', "light": ' + str(light) + ', "ldrStatus": ' + str(ldrStatus) + ', "soilMoisture": ' + str(soilMoisture) + ', "soilMoistureStatus": ' + str(soilMoistureStatus) + ', "waterPumpStatus": ' + str(waterPumpStatus) + '}'
    #sender(jsonstr, server_addrs_send)
    #testReceiveAck(receiver()) # wait for ack
    s_send.sendto(jsonstr, server_addrs_send)
    return

def collectRoomData():
    global humidity, temperature, DHT_SENSOR, DHT_PIN
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN);
    print((humidity, temperature))
    return

def requestPotData(): #Ask the arduino for the potData
    ser.write(("E,").encode("utf-8"))
    startTime = time.time()
    while time.time() < (startTime + 2):
        potData = ser.readline()
        if (len(potData) > 0):
            potData = potData.decode().strip('\r\n')
            ser.write(("0,").encode("utf-8"))
            return potData
        else:
            ser.write(("E,").encode("utf-8"))
    return('{"opcode": null, "potID": null,"waterPumpStatus": null,"waterDistance": null,"waterDistanceStatus": null,"light": null,"ldrStatus": null,"soilMoisture": null,"soilMoistureStatus": null}')

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

    print("POTID: " + str(potID))
    print(waterDistance)
    print(waterDistanceStatus)
    print(light)
    print(ldrStatus)
    print(soilMoisture)
    print(soilMoistureStatus)
    print(waterPumpStatus)
    return

def receiver():
    global s_receive
    buf, address = s_receive.recvfrom(8008)
    return (buf)

def startWaterPump(pumpDuration):
    if type(pumpDuration) is int and pumpDuration >= 1:
        pumpMessage = "C," + str(pumpDuration)
        ser.write((pumpMessage).encode("utf-8"))
    else:
        raise ValueError("Pump duration must be an integer AND must be greater than or equal to 1")
    return

def checkPotDataForErrors():
    errorArray = [0] * 11
    errorFlag = False
    if ldrStatus == 0:
        errorArray[5] = 1
        errorFlag = True
    if soilMoistureStatus == 0:
        errorArray[7] = 1
        errorFlag = True
    if waterDistanceStatus == 0:
        errorArray[8] = 1
        errorFlag = True
    if waterPumpStatus == 0:
        errorArray[9] = 1
        errorFlag = True
    if errorFlag:    
        return errorArray
    else:
        return False
       
setRoomPi()


message = requestPotData()
ser.flushInput()
message = json.loads(message)

if message.get('opcode') == '8':
    getPotData(message) #puts data into variables
    collectRoomData() #collect room data and puts into variables
    #testRoomSensors() #test room sensors for errors, if error send error to global (receive ack)
    sendSensoryData() #send the data to global and receive ack
   

while(1):
    message = receiver()
    message = json.loads(message)
    if (message.get('opcode') == "4"): #2 startwaterpump
        print("start water pump")
        startWaterPump(int(message.get("pumpDuration")))
