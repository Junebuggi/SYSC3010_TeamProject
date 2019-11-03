import serial
import time

ser = serial.Serial('/dev/tty.usbmodem144101', 9600)
    
ser.baudrate=9600
ser.flushInput() 

nPacket = 0

while True:
   # tdate = str(date.today())
    #ttime = str(datetime.now().strftime("%H:%M:%S"))
    
    data=ser.readline().decode().strip('\r\n').split(",")
    if str(data[0]) == "8" and str(nPacket) == str(data[1]):
        #message = "00" + "," + str(data[1]) + ","
        #ser.write( bytes("00", 'utf-8'))
        #ser.write(bytes(",", 'utf-8'))
        #ser.write(bytes(str(data[1]), 'utf-8'))
        #ser.write(bytes(",", 'utf-8'))
        ack = "00," + str(nPacket) + "\0"
        ser.write(ack.encode("utf-8"))
        time.sleep(0.2)
        #ser.write(str.encode(str())
        print(data)
        print(nPacket)
        nPacket = (nPacket + 1) % 100
    
    #Database table: <RoomID>, <Light>, <Humidity>, <Temperature>, <Heat Index>, <Date>, <Time>
    #cursor.execute("insert into sensorData values (" + str(data[0]) + ", '" + str(data[1]) + "', '" + str(data[2]) + "', '" + str(data[3]) + "', '" + str(data[4]) + "', '" + date + "', '" + ttime + "')");
    #dbconnect.commit();
