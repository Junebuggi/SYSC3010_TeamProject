#Autho: Abeer Rafiq
#Modified: 10/24/2019
#Source: https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/
#Source: https://pymotw.com/2/socket/udp.html

#Importing Packages
import socket, sys, time
import RPi.GPIO as GPIO
import Adafruit_DHT

#Initializing  GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) #Red LED

#Function to blink a certain PIN
def blink(pin):
    GPIO.output(pin, True)  
    time.sleep(1)  
    GPIO.output(pin, False)  
    time.sleep(1)  
    return

#Itnializing host, sockets and ports
host = sys.argv[1]
textport = sys.argv[2]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

#Intializing Temperature and Humidity Sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#Repeat
while 1:
    #Read humidity and temperature
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        #Print measurements and store into a string
        print("PotID=1, Temp={0:0.1f}*C, Humidity={1:0.1f}%".format(temperature, humidity))
        data = str("PotID=1, Temp={0:0.1f}*C, Humidity={1:0.1f}%".format(temperature, humidity))
        s.sendto(data.encode('utf-8'), server_address)
    else:
        #If no data was retrieved blink Red LED to represent an error 
        print("Failed to retrieve data from humidity sensor")
        blink(17)
        
#Shutdown socket
s.shutdown(1)

