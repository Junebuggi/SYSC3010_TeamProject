import serial
import RPi.GPIO as GPIO
import time
import sqlite3
from datetime import datetime, date

GPIO.setwarnings(False)
#connect to database file
dbconnect = sqlite3.connect("/home/pi/Documents/Team_Project/dataBases/plantNurseryDB.db");
dbconnect.row_factory = sqlite3.Row;
cursor = dbconnect.cursor();

try:
    ser = serial.Serial("/dev/ttyACM1", 9600)
except: 
    ser = serial.Serial("/dev/ttyACM0", 9600)
    
ser.baudrate=9600
def blink(pin):
    GPIO.output(pin,GPIO.HIGH)  
    time.sleep(1)  
    GPIO.output(pin,GPIO.LOW)  
    time.sleep(1)  
    return
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
while True:
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    
    data=ser.readline().decode().strip('\r\n').split(",")
    print(data)
    
    #Database table: <RoomID>, <Light>, <Humidity>, <Temperature>, <Heat Index>, <Date>, <Time>
    
    cursor.execute("insert into sensorData values (" + str(data[0]) + ", '" + str(data[1]) + "', '" + str(data[2]) + "', '" + str(data[3]) + "', '" + str(data[4]) + "', '" + date + "', '" + ttime + "')");
    
    dbconnect.commit();
