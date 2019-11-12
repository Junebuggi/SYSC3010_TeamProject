import serial
import time
import json

ser = serial.Serial('/dev/tty.usbmodem146101', 9600, timeout = 5)

ser.baudrate = 9600
ser.flushInput()

nPacket = 0

start = time.time()


while True:
    # tdate = str(date.today())
    # ttime = str(datetime.now().strftime("%H:%M:%S"))
    message = input("C,waterPumpDuration or E? ")

    if(message[0] == 'C') :
        pumpString = message + "\n"
        ser.write((pumpString).encode("utf-8"))  # start water pump message
    elif (message[0] == 'E'):
        ser.write(("E,").encode("utf-8"))  # start water pump message
        while (ser.inWaiting()):
            x = 1
        data = ser.readline().decode().strip('\r\n')

        if (len(data) > 0):
            ser.write(("0,").encode("utf-8"))
            print(data)


    ser.flushInput()
    time.sleep(0.2)


S
        
       # if str(data['opcode']) == "8":
        ##     # message = "00" + "," + str(data[1]) + ","
                #ser.write( bytes("0\n", 'utf-8'))
    ##     # ser.write(bytes(",", 'utf-8'))
    ##     # ser.write(bytes(str(data[1]), 'utf-8'))
    ##     # ser.write(bytes(",", 'utf-8'))
    ##     ack = "0\0"
    ##     ser.write(ack.encode("utf-8"))
    ##     time.sleep(0.2)
    ##     # ser.write(str.encode(str())
    ##
        #print(data)
        #print(nPacket)
        #nPacket = (nPacket + 1) % 100

    # Database table: <RoomID>, <Light>, <Humidity>, <Temperature>, <Heat Index>, <Date>, <Time>
    # cursor.execute("insert into sensorData values (" + str(data[0]) + ", '" + str(data[1]) + "', '" + str(data[2]) + "', '" + str(data[3]) + "', '" + str(data[4]) + "', '" + date + "', '" + ttime + "')");
    # dbconnect.commit();
