#Source: https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

#Importing Packages
import Adafruit_DHT

#Intializing Temperature and Humidity Sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#Repeat
while True:
    #Read humidity and temperature
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        #Print measurements and store into a string
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
         #If no data was retrieved blink Red LED to represent a error
        print("Failed to retrieve data from humidity sensor")