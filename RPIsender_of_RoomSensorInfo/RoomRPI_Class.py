#Author: Abeer Rafiq
#Modified: 11/24/2019 9:08 am

#Importing Packages
import socket, sys, time, json, serial, Adafruit_DHT
import RPi.GPIO as GPIO
from datetime import datetime, date
import Adafruit_CharLCD as LCD

#Creating a room rpi class
class RoomRPI:
    #The constructor
    def __init__(self, port, server_ip_addrs):
        #Setting port
        self.__port = int(port)
        #Setting room ID
        self.__roomID = 1
        #Setting socket to receive
        self.__soc_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_address = ('', self.__port)
        self.__soc_recv.bind(recv_address)
        self.__soc_recv.settimeout(2)
        #Setting socket/addresses to send to the global rpi
        self.__soc_send =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server_addrs = (server_ip_addrs, self.__port)
        #Setting up led blinking
        self.__receiveLED = 14
        self.__sendLED = 15
        self.__errorLED = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__receiveLED, GPIO.OUT)
        GPIO.setup(self.__sendLED, GPIO.OUT)
        GPIO.setup(self.__errorLED, GPIO.OUT)
        #Setting up string for acknowldegements
        self.__ackstr = "{'opcode':'0'}"
        #Setting serial for arduino
        self.__ser = serial.Serial('/dev/ttyACM0', timeout = 0.1)
        self.__ser.flushInput()
        #Setting up pins for temp/humidity sensor
        self.__DHT_SENSOR = Adafruit_DHT.DHT22
        self.__DHT_PIN = 4
        # Setting up pins for the LCD
        lcd_rs        = 25  
        lcd_en        = 24
        lcd_d4        = 23
        lcd_d5        = 17
        lcd_d6        = 18
        lcd_d7        = 22
        lcd_backlight = 4
        # Define LCD column and row size for 16x2 LCD.
        lcd_columns = 16
        lcd_rows    = 2
        #Initializing the LCD
        self.__lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, \
                     lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
        self.__lcd.show_cursor(False)
        #Setting up default sensor variables
        self.__currentLight = 0
        self.__currentSoilMoisture = 0
        self.__currentWaterDistance = 0
        self.__currentRoomHumidity = 0
        self.__currentRoomTemperature = 0
        #Setting timeout/end time values
        self.__ack_timeout = 1
        self.__ack_endTime = 4
        print("\nRoom RPI Initialized")
    
    #To blink a pin once
    def blink(self, pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        return
    
    #To send msgs to the global server
    def send_server_msg(self, message):
        self.__soc_send.sendto(message, self.__server_addrs)
        #Blink send LED
        self.blink(self.__sendLED)
        print("\nMessage sent to Server: " + message)
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
    
    #To check if temp/humidity sensor is working
    def testRoomSensors(self):
        if self.__currentRoomHumidity is None and self.__currentRoomTemperature is None:
            #Call error detected to handle error
            self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 1, 0, 0, 0"}')
            #Blink LED
            self.blink(self.__errorLED)
            #Set temp and humidity to 0 if sensor isn't working
            self.__currentRoomTemperature = 0
            self.__currentRoomHumidity = 0
        print("\nDHT22 has been Tested")
        return
    
    #To send error to the server
    def errorDetected(self, error):
        #If ack received return
        if (self.send_server_msg(error) == False):
            #If no ack received, try sending again
            print("\nError sent again to server")
            self.errorDetected(error)
        return

    #To get measurements from DHT22 sensor for humidity and temp
    def collectRoomData(self):
        self.__currentRoomHumidity, self.__currentRoomTemperature = \
                                    Adafruit_DHT.read(self.__DHT_SENSOR, self.__DHT_PIN);
        print("\nRoom Data Variables Updated")

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
        #Arduino's sensor error variables
        waterDistanceStatus = potData.get('waterDistanceStatus')
        soilMoistureStatus = potData.get('soilMoistureStatus')
        waterPumpStatus = potData.get('waterPumpStatus')
        ldrStatus = potData.get('ldrStatus')
        waterLow = potData.get('waterLow')
        #If any status == 0, means there is an error, call errorDetected
        #Set associating measurement to 0 if there is one
        if ldrStatus == 0:
           light = 0
           self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 1, 0, 0, 0, 0"}')
        if soilMoistureStatus == 0:
           soilMoisture = 0
           self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 0, 1, 0, 0"}')
        if waterDistanceStatus == 0:
           self.waterDistance = 0
           errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 0, 0, 1, 0"}')
        if waterPumpStatus == 0:
           self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 0, 0, 0, 0, 0, 1"}')
        if waterLow == 0:
           self.errorDetected('{"opcode" : "D", "sensorArray" : "0, 0, 0, 0, 1, 0, 0, 0, 0, 0"}')
        print("\nPot Data Variables Updated")
        return potID

    #To create JSON with all data and send to global server
    def sendSensoryData(self, potID):
        alldata = '{"opcode": "9", "roomID": ' + str(self.__roomID) + \
                  ', "potID": ' + str(potID) + ', "temperature": ' + \
                  str(self.__currentRoomTemperature) + ', "humidity": ' + \
                  str(self.__currentRoomHumidity) + ', "waterDistance": ' + \
                  str(self.__currentWaterDistance) + ', "waterDistanceStatus": ' + \
                  ', "light": ' + str(self.__currentLight) + ', "soilMoisture": ' + \
                  str(self.__currentSoilMoisture) + '}'
        #If ack received return
        if (self.send_server_msg(alldata) == False):
            #If no ack received, send data again
            print("\nAll data sent again to server")
            self.sendSensoryData(potID)
        return
    
    #To communicate to the arduino to send it's sensory data
    def requestPotData(self):
        print("\nRequesting Pot Data")
        self.__ser.write(("E,").encode("utf-8"))
        startTime = time.time()
        while time.time() < (startTime + 2):
            #readLine to get data
            potData = ser.readline()
            self.blink(self.__receiveLED)
            if (len(potData) > 0):
                potData = potData.decode().strip('\r\n')
                #send acknowledgement
                self.__ser.write(("0,").encode("utf-8"))
                self.blink(self.__sendLED)
                print("Received Pot Data: " + potData)
                return potData
            else:
                #send error
                self.__ser.write(("E,").encode("utf-8"))
        return('{"opcode": null, "potID": null,"waterPumpStatus": null,"waterDistance": null,"waterDistanceStatus": null,"light": null,"ldrStatus": null,"soilMoisture": null,"soilMoistureStatus": null}')

    #To create JSON to start water pump and communicate to arduino
    def startWaterPump(self, pumpDuration):
        if type(pumpDuration) is int and pumpDuration >= 1:
            #Creating json, writing to serial
            pumpMessage = "C," + str(pumpDuration)
            self.blink(self.__sendLED)
            self.__ser.write((pumpMessage).encode("utf-8"))
        else:
            #Error is raised
            raise ValueError("Pump duration must be an integer AND must be greater than or equal to 1")
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


#Main function which receives json data/arduino data and invokes methods based on opcode
def main():
    #Create room RPI object (port, server_ip_addrs)
    roomRPI = RoomRPI(1000, '192.168.1.47')
    startTime = time.time()
    sendTime = 5
    while True:
        #Request arduino data after every 'sendTime' seconds
        if time.time() > (startTime + sendTime):
            message = self.requestPotData()
            message = json.loads(message)
            #Ensure the opcode received is 8 (arduino sent pot data)
            if message.get('opcode') == '8':
                #Update pot variables
                potID = self.getPotData(message)
                #Update room variables by getting DHT22 measurements
                self.collectRoomData()
                #Test if DHT22 is working
                self.testRoomSensors()
                #Send all data to server
                self.sendSensoryData(potID)
            #Recalculate time
            startTime = time.time()
        else:
            #Check to see if server sent a start water pump msg
            try:
                message = roomRPI.receive()
            #If no msg sent from server, time out 
            except socket.timeout, e:
                err = e.args[0]
                if err == 'timed out':
                    time.sleep(1)
                    print('\nReceiver timed out')
                    continue
            if (message ==  False):
                #If length of buffer is <1
                continue
            else:
                message = json.loads(message)
                #To start water pump
                if (message.get('opcode') == "4"): 
                    startWaterPump(int(message.get("pumpDuration")))
                else:
                    continue

    self.__soc_recv.shutdown(1)
    self.__soc_send.shutdown(1)
    return
    
if __name__== "__main__":
    main()
