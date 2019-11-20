#Author: Abeer Rafiq
#Last Modified: November, 20, 2019

def checkUserThresholds(testInput=None):
    global lightThreshold, soilMoistureThreshold, roomHumidityThreshold, roomTemperatureThreshold
    global lightLessGreaterThan, soilMoistureLessGreaterThan, roomHumidityLessGreaterThan, roomTemperatureLessGreaterThan
    global light, soilMoisture, temperature, humidity
    
    if testInput != None:
        lightThreshold = testInput.get("lightThreshold")
        soilMoistureThreshold = testInput.get("soilMoistureThreshold")
        roomHumidityThreshold = testInput.get("roomHumidityThreshold")
        roomTemperatureThreshold = testInput.get("roomTemperatureThreshold")
        
        lightLessGreaterThan = testInput.get("lightLessGreaterThan")
        soilMoistureLessGreaterThan = testInput.get("soilMoistureLessGreaterThan")
        roomHumidityLessGreaterThan = testInput.get("roomHumidityLessGreaterThan")    
        roomTemperatureLessGreaterThan = testInput.get("roomTemperatureLessGreaterThan")    
        
        light = testInput.get("light")
        soilMoisture = testInput.get("soilMoisture")
        temperature = testInput.get("temperature")
        humidity = testInput.get("humidity")

    a = '{"opcode" : "D", "sensorArray" : "1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0"}' #light
    b = '{"opcode" : "D", "sensorArray" : "0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0"}' #roomHumidity
    c = '{"opcode" : "D", "sensorArray" : "0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0"}' #roomTemp
    d = '{"opcode" : "D", "sensorArray" : "0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0"}{"opcode" : "4", "pumpDuration" : "2.0"}' #soilMoisture

    errorTypes = [a, b, c, d]
    errorCombined = ""
    
    if lightLessGreaterThan == ">":
        if light > lightThreshold:
            if testInput is None:
                notifyUser(errorTypes[0])
            else:
                errorCombined = errorCombined + errorTypes[0]
    elif lightLessGreaterThan == "<":
        if light < lightThreshold:
            if testInput is None:
                notifyUser(errorTypes[0])
            else:
                errorCombined = errorCombined + errorTypes[0]
    if roomHumidityLessGreaterThan == ">":
        if humidity > roomHumidityThreshold:
            if testInput is None:
                notifyUser(errorTypes[1])
            else:
                errorCombined = errorCombined + errorTypes[1]
    elif roomHumidityLessGreaterThan == "<":
        if humidity < roomHumidityThreshold:
            if testInput is None:
                notifyUser(errorTypes[1])
            else:
                errorCombined = errorCombined + errorTypes[1]
    if roomTemperatureLessGreaterThan == ">":
        if temperature > roomTemperatureThreshold:
            if testInput is None:
                notifyUser(errorTypes[2])
            else:
                errorCombined = errorCombined + errorTypes[2]
    elif roomTemperatureLessGreaterThan == "<":
        if temperature < roomTemperatureThreshold:
            if testInput is None:
                notifyUser(errorTypes[2])
            else:
                errorCombined = errorCombined + errorTypes[2]
    if soilMoistureLessGreaterThan == ">":
        if soilMoisture > soilMoistureThreshold:
            if testInput is None:
                message = errorTypes[3].split("}{")             	
                notifyUser(message[0] + '}')
                startWaterPump('{' + message[1]) 
                notifyUser('{' + message[1])
            else:
                errorCombined = errorCombined + errorTypes[3]
    elif soilMoistureLessGreaterThan == "<":
        if soilMoisture < soilMoistureThreshold:
            if testInput is None:
                message = errorTypes[3].split("}{")             	
                notifyUser(message[0] + '}')
                startWaterPump('{' + message[1]) 
                notifyUser('{' + message[1])
            else:
                errorCombined = errorCombined + errorTypes[3]
    if testInput != None:
        return errorCombined 
    return

def checkUserThresholds_LightHighTest():
    testInput = {"lightThreshold" : 50.5, "lightLessGreaterThan" : ">", "light" : 60, "roomHumidityThreshold" : 50.5, "roomHumidityLessGreaterThan" : ">", "humidity" : 45, "roomTemperatureThreshold" : 50.5, "roomTemperatureLessGreaterThan" : ">", "temperature" : 45, "soilMoistureThreshold" : 50.5, "soilMoistureLessGreaterThan" : ">",  "soilMoisture" : 45}
    expectedOutput = '{"opcode" : "D", "sensorArray" : "1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0"}'
    output = checkUserThresholds(testInput)

    print("\n ****************************  Testing CheckUserThresholds() when Light is too High  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS ")
    else:
        print ("Result: FAIL ")
        print ("Received: " + output)
    return

def checkUserThresholds_LightLowTest():
    testInput = {"lightThreshold" : 50.5, "lightLessGreaterThan" : "<", "light" : 45, "roomHumidityThreshold" : 50.5, "roomHumidityLessGreaterThan" : ">", "humidity" : 45, "roomTemperatureThreshold" : 50.5, "roomTemperatureLessGreaterThan" : ">", "temperature" : 45, "soilMoistureThreshold" : 50.5, "soilMoistureLessGreaterThan" : ">",  "soilMoisture" : 45}
    expectedOutput = '{"opcode" : "D", "sensorArray" : "1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0"}'
    output = checkUserThresholds(testInput)

    print("\n ****************************  Testing CheckUserThresholds() when Light is too Low  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS ")
    else:
        print ("Result: FAIL ")
        print ("Received: " + output)
    return


def checkUserThresholds_RoomHumidityHighTest():
    testInput = {"lightThreshold" : 50.5, "lightLessGreaterThan" : ">", "light" : 45, "roomHumidityThreshold" : 50.5, "roomHumidityLessGreaterThan" : ">", "humidity" : 60, "roomTemperatureThreshold" : 50.5, "roomTemperatureLessGreaterThan" : ">", "temperature" : 45, "soilMoistureThreshold" : 50.5, "soilMoistureLessGreaterThan" : ">",  "soilMoisture" : 45}
    expectedOutput = '{"opcode" : "D", "sensorArray" : "0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0"}'
    output = checkUserThresholds(testInput)

    print("\n ****************************  Testing CheckUserThresholds() when Room Humidity is too High  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS ")
    else:
        print ("Result: FAIL ")
        print ("Received: " + output)
    return
    
def checkUserThresholds_RoomHumidityLowTest():
    testInput = {"lightThreshold" : 50.5, "lightLessGreaterThan" : ">", "light" : 45, "roomHumidityThreshold" : 50.5, "roomHumidityLessGreaterThan" : "<", "humidity" : 45, "roomTemperatureThreshold" : 50.5, "roomTemperatureLessGreaterThan" : ">", "temperature" : 45, "soilMoistureThreshold" : 50.5, "soilMoistureLessGreaterThan" : ">",  "soilMoisture" : 45}
    expectedOutput = '{"opcode" : "D", "sensorArray" : "0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0"}'
    output = checkUserThresholds(testInput)

    print("\n ****************************  Testing CheckUserThresholds() when Room Humidity is too Low  ****************************")
    print("Input: ")    
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS ")
    else:
        print ("Result: FAIL ")
        print ("Received: " + output)
    return
    
def checkUserThresholds_RoomTemperatureHighTest():
    testInput = {"lightThreshold" : 50.5, "lightLessGreaterThan" : ">", "light" : 45, "roomHumidityThreshold" : 50.5, "roomHumidityLessGreaterThan" : ">", "humidity" : 45, "roomTemperatureThreshold" : 50.5, "roomTemperatureLessGreaterThan" : ">", "temperature" : 60, "soilMoistureThreshold" : 50.5, "soilMoistureLessGreaterThan" : ">",  "soilMoisture" : 45}
    expectedOutput = '{"opcode" : "D", "sensorArray" : "0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0"}'
    output = checkUserThresholds(testInput)

    print("\n ****************************  Testing CheckUserThresholds() when Room Temperature is too High  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS ")
    else:
        print ("Result: FAIL ")
        print ("Received: " + output)
    return
    
def checkUserThresholds_RoomTemperatureLowTest():
    testInput = {"lightThreshold" : 50.5, "lightLessGreaterThan" : ">", "light" : 45, "roomHumidityThreshold" : 50.5, "roomHumidityLessGreaterThan" : ">", "humidity" : 45, "roomTemperatureThreshold" : 50.5, "roomTemperatureLessGreaterThan" : "<", "temperature" : 45, "soilMoistureThreshold" : 50.5, "soilMoistureLessGreaterThan" : ">",  "soilMoisture" : 45}
    expectedOutput = '{"opcode" : "D", "sensorArray" : "0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0"}'
    output = checkUserThresholds(testInput)

    print("\n ****************************  Testing CheckUserThresholds() when Room Temperature is too Low  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS ")
    else:
        print ("Result: FAIL ")
        print ("Received: " + output)
    return

def checkUserThresholds_SoilMoistureHighTest():
    testInput = {"lightThreshold" : 50.5, "lightLessGreaterThan" : ">", "light" : 45, "roomHumidityThreshold" : 50.5, "roomHumidityLessGreaterThan" : ">", "humidity" : 45, "roomTemperatureThreshold" : 50.5, "roomTemperatureLessGreaterThan" : ">", "temperature" : 45, "soilMoistureThreshold" : 50.5, "soilMoistureLessGreaterThan" : ">",  "soilMoisture" : 60}
    expectedOutput = '{"opcode" : "D", "sensorArray" : "0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0"}' + '{"opcode" : "4", "pumpDuration" : "2.0"}'
 
    output = checkUserThresholds(testInput)

    print("\n ****************************  Testing CheckUserThresholds() when Soil Moisture is too High  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS ")
    else:
        print ("Result: FAIL ")
        print ("Received: " + output)
    return

def checkUserThresholds_SoilMoistureLowTest():
    testInput = {"lightThreshold" : 50.5, "lightLessGreaterThan" : ">", "light" : 45, "roomHumidityThreshold" : 50.5, "roomHumidityLessGreaterThan" : ">", "humidity" : 45, "roomTemperatureThreshold" : 50.5, "roomTemperatureLessGreaterThan" : ">", "temperature" : 45, "soilMoistureThreshold" : 50.5, "soilMoistureLessGreaterThan" : "<",  "soilMoisture" : 45}
    expectedOutput = '{"opcode" : "D", "sensorArray" : "0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0"}' + '{"opcode" : "4", "pumpDuration" : "2.0"}'
 
    output = checkUserThresholds(testInput)

    print("\n ****************************  Testing CheckUserThresholds() when Soil Moisture is too Low ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS ")
    else:
        print ("Result: FAIL ")
        print ("Received: " + output)
    return

checkUserThresholds_LightHighTest()
input("")
checkUserThresholds_LightLowTest()
input("")
checkUserThresholds_RoomHumidityHighTest()
input("")
checkUserThresholds_RoomHumidityLowTest()
input("")
checkUserThresholds_RoomTemperatureHighTest()
input("")
checkUserThresholds_RoomTemperatureLowTest()
input("")
checkUserThresholds_SoilMoistureHighTest()
input("")
checkUserThresholds_SoilMoistureLowTest()
