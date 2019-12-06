#Author: Abeer Rafiq
#Modified: 12/6/2019 12pm

#Importing Packages
import socket, sys, time, json, serial, Adafruit_DHT
import RPi.GPIO as GPIO
from datetime import datetime, date
import Adafruit_CharLCD as LCD
import random

#Creating a room rpi class
class RoomRPI:
    #The constructor
    def __init__(self, port, server_ip_addrs, debug):
        #Setting port
        self.__port = int(port)
        #Setting room ID
        self.__roomID = 1
        #Setting timeout/end time values
        self.__ack_timeout = 10
        self.__ack_endTime = 20
        #Setting whether to show print statement or not
        self.__DEBUG = debug
        #Setting socket to receive
        self.__soc_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_address = ('', self.__port)
        self.__soc_recv.bind(recv_address)
        self.__soc_recv.settimeout(self.__ack_timeout)
        #Setting socket/addresses to send to the global rpi
        self.__soc_send =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server_addrs = (server_ip_addrs, self.__port)
        #Setting up led blinking which blink to signify errors
        self.__receiveLED = 16 #to show error in receiving
        self.__sendLED = 20 #to show ack received
        self.__errorLED = 21 #to show temp/humidity sensor not working
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__receiveLED, GPIO.OUT)
        GPIO.setup(self.__sendLED, GPIO.OUT)
        GPIO.setup(self.__errorLED, GPIO.OUT)
        #Setting up string for acknowldegements
        self.__ackstr = '{"opcode":"0"}'
        #Setting serial for arduino, if no serial print error and exit
        try:
            self.__ser = serial.Serial('/dev/ttyACM0', timeout = 0.1)
        except serial.serialutil.SerialException:
            if(DEBUG):
                print("Error! No Arduino Connected!")
                sys. exit(0)
        self.__ser.flushInput()
        #Setting up pins for temp/humidity sensor
        self.__DHT_SENSOR = Adafruit_DHT.DHT22
        self.__DHT_PIN = 4
        #Setting up pins for the LCD
        lcd_rs = 25  
        lcd_en = 24
        lcd_d4 = 23
        lcd_d5 = 17
        lcd_d6 = 18
        lcd_d7 = 22
        lcd_backlight = 2
        #Define LCD column and row size for 16x2 LCD.
        lcd_columns = 16
        lcd_rows = 2
        #Initializing the LCD
        self.__lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, \
                     lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
        self.__lcd.show_cursor(False)
        self.__lcd.message('RoomPi BootingUp\nPrepare4Awesome!')
        #Setting up default sensor variables
        self.__currentLight = 0
        self.__currentSoilMoisture = 0
        self.__currentWaterDistance = 0
        self.__currentRoomHumidity = 0
        self.__currentRoomTemperature = 0
        self.__currentWaterDistanceStatus = 0
        self.__currentWaterPumpStatus = 0
        self.__currentSoilMoistureStatus = 0
        self.__currentWaterLow = 0
        #Number of times to keep resending a msg if ack not received
        self.__numRetries = 1
        if (self.__DEBUG):
            print("\nRoom RPI Initialized")
    
    #Receives/returns buffer and sends ack
    def receive(self):
        #Receives
        if (self.__DEBUG):
            print("\nWaiting to receive on port %d ... " % self.__port)
        #Try loading buffer, if error send no ack and blink receive LED to show error
        try:
            buf, address = self.__soc_recv.recvfrom(self.__port)
            buf = json.loads(str(buf))
            #Check to see if nothing received
            if len(buf) > 0:
                if (self.__DEBUG):
                    print ("Received %s bytes from '%s': %s " % (len(buf), address[0], buf))
                #Sending ack
                self.__soc_send.sendto(self.__ackstr, (address[0], self.__port))
                if (self.__DEBUG):
                    print ("Sent %s to %s" % (self.__ackstr, (address[0], self.__port)))
                return buf
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
        
    #To blink a pin once
    def blink(self, pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        return
    
    #To send msgs to the global server
    def send_server_msg(self, message):
        self.__soc_send.sendto(message.encode("utf-8"), self.__server_addrs)
        #Blink send LED
        self.blink(self.__sendLED)
        if (self.__DEBUG):
            print("\nMessage sent to Server: " + message)
        #Should be receiving an ack so timeout if no ack received
        self.__soc_recv.settimeout(self.__ack_timeout)
        startTime = time.time()
        endTime = self.__ack_endTime
        while (True):
            #If less than a endTime amount of time
            if time.time() < (startTime + endTime):
                try:
                    #Try Receving otherwise timeout and retry
                    if (self.__DEBUG):
                        print("Waiting for Acknowledgement . . .")
                    buf, address = self.__soc_recv.recvfrom(self.__port)
                    #If buf is received, try to load it
                    buf = json.loads(str(buf))
                    if not len(buf):
                        #No ack received, retry
                        continue
                    else:
                        if (buf.get("opcode") == '0'):
                            #Ack recevied!
                            if (self.__DEBUG):
                                print("Acknowledgement Received")
                            self.blink(self.__sendLED)
                            time.sleep(2)
                            return True
                        else:
                            #No ack received, retry
                            continue
                except socket.timeout:
                    if (self.__DEBUG):
                        print("Receiving is Timed Out")
                    #Restart while loop (Retry)
                    continue
                except (ValueError, KeyError, TypeError), e:
                    if (self.__DEBUG):
                        print(str(e))
                    #Ack not received, try again
                    continue
            else:
                #Failed to receive ack within a endTime amount of time
                return False
        return
    
    #To check if temp/humidity sensor is working
    def testRoomSensors(self):
        if self.__currentRoomHumidity is None and self.__currentRoomTemperature is None:
            #Call error detected to handle error
            self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 1, 0, 0, 0"}')
            #Blink LED
            self.blink(self.__errorLED)
            #Set temp and humidity to 0 if sensor isn't working
            self.__currentRoomTemperature = 1
            self.__currentRoomHumidity = 1
        if (self.__DEBUG):
            print("\nDHT22 has been Tested")
        return
    
    #To send error to the server
    def errorDetected(self, error):
        #If ack received, try sending again for certain number of times
        i = 0
        while(i <= self.__numRetries):
            if (i == 0):
                if(self.__DEBUG):
                    print("Msg has been sent to the Global Server")
            else:
                if(self.__DEBUG):
                    print("Msg is being sent again to the Global Server")
            if (self.send_server_msg(error) == True):
                #Ack has been received, return
                if (self.__DEBUG):
                    print("Msg has been received by Global Server")
                return
            else:
                #If no ack received, try sending again
                if (self.__DEBUG):
                    print("Msg has not been by Global Server")
            i = i + 1
        #Msg has been sent numRetries times, return
        if (self.__DEBUG):
            print("Msg was not received by Global Server")
        return
    
    #To get measurements from DHT22 sensor for humidity and temp
    def collectRoomData(self):
        self.__currentRoomHumidity, self.__currentRoomTemperature = \
                                    Adafruit_DHT.read(self.__DHT_SENSOR, self.__DHT_PIN);
        if (self.__DEBUG):
            print("\nRoom Data Variables Updated")
        if self.__currentRoomHumidity != None and self.__currentRoomTemperature != None:
            #Round Values
            self.__currentRoomHumidity = round(float(str(self.__currentRoomHumidity)), 2)
            self.__currentRoomTemperature =  round(float(str(self.__currentRoomTemperature)), 2)
            self.__lcd.clear()
            self.__lcd.message("Temp: " + str(self.__currentRoomTemperature) + chr(223) + "C\nHumidity: " + str(self.__currentRoomHumidity) + "%")
        return

    #To set current pot sensor values to what has been detected by pot sensors
    #Also to handle arduino's sensor errors
    def getPotData(self, potData):
        potID = int(potData.get('potID'))
        #Arduino sensor values
        self.__currentWaterDistance = potData.get('waterDistance')
        self.__currentSoilMoisture = potData.get('soilMoisture')
        self.__currentLight = potData.get('light')
        self.__currentWaterDistanceStatus = potData.get('waterDistanceStatus')
        self.__currentWaterPumpStatus = potData.get('waterPumpStatus')
        self.__currentWaterLow = potData.get('waterLow')
        self.__currentSoilMoistureStatus = potData.get('soilMoistureStatus')
        #Arduino's sensor error variables
        ldrStatus = potData.get('ldrStatus')
        #If any status == 0, means there is an error, call errorDetected
        #Set associating measurement to 0 if there is one
        if ldrStatus == 0:
           light = 0
           self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 1, 0, 0, 0, 0"}')
        if self.__currentWaterLow == 0:
           soilMoisture = 0
           self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 1, 0, 0, 0, 0, 0"}')
        if self.__currentSoilMoistureStatus == 0:
           soilMoisture = 0
           self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 0, 1, 0, 0"}')
        if self.__currentWaterDistanceStatus == 0:
           self.waterDistance = 0
           self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 0, 0, 1, 0"}')
        if self.__currentWaterPumpStatus == 0:
           self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 0, 0, 0, 1"}')
        if (self.__DEBUG):
            print("\nPot Data Variables Updated")
        return potID

    #To create JSON with all data and send to global server
    def sendSensoryData(self, potID):
        alldata = '{"opcode": "9", "roomID": ' + str(self.__roomID) + \
                  ', "potID": ' + str(potID) + ', "temperature": ' + \
                  str(self.__currentRoomTemperature) + ', "humidity": ' + \
                  str(self.__currentRoomHumidity) + ', "waterDistance": ' + \
                  str(self.__currentWaterDistance) + ', "waterDistanceStatus": ' + \
                  str(self.__currentWaterDistanceStatus) + ', "light": ' + str(self.__currentLight) + ', "soilMoisture": ' + \
                  str(self.__currentSoilMoisture) + '}'
         #If ack received, try sending again for certain number of times
        i = 0
        while(i <= self.__numRetries):
            if (self.send_server_msg(alldata) == True):
                #Ack has been received, return
                if (self.__DEBUG):
                    print("Msg sent to Global Server")
                return
            else:
                #If no ack received, try sending again
                if (self.__DEBUG):
                    print("Msg not received by Global")
            i = i + 1
        return  
       
    #To communicate to the arduino to send it's sensory data
    def requestPotData(self):
        if (self.__DEBUG):
            print("\nRequesting Pot Data")
        self.__ser.write(("E,").encode("utf-8"))
        startTime = time.time()
        while time.time() < (startTime + 2):
            #readLine to get data
            potData = self.__ser.readline()
            if (len(potData) > 0):
                potData = potData.decode().strip('\r\n')
                #send acknowledgement
                self.__ser.write(("0,").encode("utf-8"))
                if (self.__DEBUG):
                    print("Received Pot Data: " + str(potData))
                return potData
            else:  
                #send error
                self.__ser.write(("E,").encode("utf-8"))
        return('{"opcode": null, "potID": null,"waterPumpStatus": null,"waterDistance": null,"waterDistanceStatus": null,"light": null,"ldrStatus": null,"soilMoisture": null,"soilMoistureStatus": null}')
        
    #To create JSON to start water pump and communicate to arduino
    def startWaterPump(self, pumpDuration):
        if(self.__currentSoilMoistureStatus == 1 and self.__currentWaterLow == 1 and self.__currentWaterDistanceStatus == 1):
            if type(pumpDuration) is int and pumpDuration >= 1:
                if (self.__DEBUG):
                    print("\nStarting Water Pump!!")
                #Creating json, writing to serial
                pumpMessage = "C," + str(pumpDuration)
                self.__ser.write((pumpMessage).encode("utf-8"))
            else:
                #Error is raised
                raise ValueError("Pump duration must be an integer AND must be greater than or equal to 1")
        else:
            if (self.__DEBUG):
                print("\nWater Pump is not working! No water pump msg sent")
        return
    
#Main function which receives json data/arduino data and invokes methods based on opcode
def main():
    #Create room RPI object (port, server_ip_addrs)
    DEBUG = True
    roomRPI = RoomRPI(1003, '192.168.137.101', DEBUG)
    startTime = time.time()
    sendTime = 20
    while True:
        #Request arduino data after every 'sendTime' seconds
        if time.time() > (startTime + sendTime):
            message = roomRPI.requestPotData()
            if (DEBUG):
                print(message)
            message = json.loads(message)
            #Ensure the opcode received is 8 (arduino sent pot data)
            if message.get('opcode') == '8':
                #Update pot variables
                potID = roomRPI.getPotData(message)
                #Update room variables by getting DHT22 measurements
                roomRPI.collectRoomData()
                #Test if DHT22 is working
                roomRPI.testRoomSensors()
                #Send all data to server
                roomRPI.sendSensoryData(potID)
            #Recalculate time
            startTime = time.time()
        else:
            #Check to see if server sent a start water pump msg
            try:
                message = roomRPI.receive()
                if (message ==  None):
                    #If length of buffer is < 1
                    continue
                else:
                    #To start water pump
                    if (message.get('opcode') == "4"): 
                        roomRPI.startWaterPump(int(message.get("pumpDuration")))
                    else:
                        continue
            #If no msg sent from server, time out 
            except socket.timeout, e:
                err = e.args[0]
                if err == 'timed out':
                    if (DEBUG):
                        print('\nReceiver timed out')
                    continue
    roomRPI.__soc_recv.shutdown(1)
    roomRPI.__soc_send.shutdown(1)
    return
    
if __name__== "__main__":
    main()

   
