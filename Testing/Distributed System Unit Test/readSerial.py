import serial
import time
import json

ser = serial.Serial('/dev/tty.usbmodem144101', 9600, timeout = 0.1)

ser.baudrate = 9600
ser.flushInput()

nPacket = 0

start = time.time()

def requestPotData(): #Ask the arduino for the potData
    if (ser.isOpen() == False):
        ser.open()
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

def startWaterPump(pumpDuration):
    if type(pumpDuration) is int and pumpDuration >= 1:
        pumpMessage = "C," + str(pumpDuration) + "\n"
        ser.write((pumpMessage).encode("utf-8"))
    else:
        raise ValueError("Pump duration must be an integer AND must be greater than or equal to 1")
    return

n = 0
while n < 20:
    # tdate = str(date.today())
    # ttime = str(datetime.now().strftime("%H:%M:%S"))
    # message = input("C,waterPumpDuration or E? ")

    n = n + 1
    print(n)
    data = requestPotData()
    #data = json.loads(data)
    print(data)
    time.sleep(0.5)
    startWaterPump(3)
    #ser.write(("C,5\n").encode("utf-8"))  # start water pump message
    time.sleep(10)

    # if(message[0] == 'C') :
    #     pumpString = message + "\n"
    #     ser.write((pumpString).encode("utf-8"))  # start water pump message
    # elif (message[0] == 'E'):
    #     ser.write(("E,").encode("utf-8"))  # start water pump message
    #     flag = True
    #     startTime = time.time()
    #     while flag and (time.time() < startTime + 2):
    #         data = ser.readline()
    #         if (len(data) > 0):
    #             data = data.decode().strip('\r\n')
    #             flag = False
    #             ser.write(("0,").encode("utf-8"))
    #             print(data)
    #         else:
    #             ser.write(("E,").encode("utf-8"))



    #time.sleep(0.2)
    #ser.flushInput()
        
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
