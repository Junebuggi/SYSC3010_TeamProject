#Author: Abeer Rafiq
#Last Modified: November, 20, 2019

import time, json
from datetime import datetime, date

def setDefaultThresholds(potRegisterRequest, testingInput = None):
    global cursor
    global lightThreshold, soilMoistureThreshold, roomHumidityThreshold, roomTemperatureThreshold
    global lightLessGreaterThan, soilMoistureLessGreaterThan, roomHumidityLessGreaterThan, roomTemperatureLessGreaterThan
   
    if testingInput != None:
        lightThreshold = testingInput.get("lightThreshold")
        lightLessGreaterThan = testingInput.get("lightLessGreaterThan")
        roomHumidityThreshold = testingInput.get("roomHumidityThreshold")
        roomHumidityLessGreaterThan = testingInput.get("roomHumidityLessGreaterThan")
        roomTemperatureThreshold = testingInput.get("roomTemperatureThreshold")
        roomTemperatureLessGreaterThan = testingInput.get("roomTemperatureLessGreaterThan")
        soilMoistureThreshold = testingInput.get("soilMoistureThreshold")
        soilMoistureLessGreaterThan = testingInput.get("soilMoistureLessGreaterThan")

    if "potID" not in potRegisterRequest.keys():
        return "potID not found"
    else:
        potID = str(potRegisterRequest.get("potID"))
        tdate = str(testingInput.get("tdate"))
        ttime = str(testingInput.get("ttime"))

    thresholdValueDefault = "70"
    lessGreaterThanDefault = ">"
    
    mySQLLight = {"potID" : potID, "sensorType" : "light", "thresholdValue" : thresholdValueDefault, "lessGreaterThan" : lessGreaterThanDefault, "tdate" : tdate, "ttime" : ttime }
    mySQLSoilMoisture = {"potID" : potID, "sensorType" : "soilMoisture", "thresholdValue" : thresholdValueDefault, "lessGreaterThan" : lessGreaterThanDefault, "tdate" : tdate, "ttime" : ttime }
    mySQLRoomHumidity = {"potID" : potID, "sensorType" : "roomHumidity", "thresholdValue" : thresholdValueDefault, "lessGreaterThan" : lessGreaterThanDefault, "tdate" : tdate, "ttime" : ttime }
    mySQLRoomTemperature = {"potID" : potID, "sensorType" : "roomTemperature", "thresholdValue" : thresholdValueDefault, "lessGreaterThan" : lessGreaterThanDefault, "tdate" : tdate, "ttime" : ttime }
    
    lightThreshold = thresholdValueDefault 
    lightLessGreaterThan = lessGreaterThanDefault 
    soilMoistureThreshold = thresholdValueDefault 
    soilMoistureLessGreaterThan = lessGreaterThanDefault 
    roomHumidityThreshold = thresholdValueDefault 
    roomHumidityLessGreaterThan = lessGreaterThanDefault 
    roomTemperatureThreshold = thresholdValueDefault 
    roomTemperatureLessGreaterThan= lessGreaterThanDefault 
    
    if testingInput is None:
        updateUserThresholdsTable(mySQLLight)
        updateUserThresholdsTable(mySQLSoilMoisture)    
        updateUserThresholdsTable(mySQLRoomHumidity)
        updateUserThresholdsTable(mySQLRoomTemperature)
    else:
        newVariablesValues = {"lightThreshold" : lightThreshold,
        "lightLessGreaterThan" : lightLessGreaterThan,
        "soilMoistureThreshold" : soilMoistureThreshold,
        "soilMoistureLessGreaterThan" : soilMoistureLessGreaterThan,
        "roomHumidityThreshold" : roomHumidityThreshold, 
        "roomHumidityLessGreaterThan" : roomHumidityLessGreaterThan,
        "roomTemperatureThreshold" : roomTemperatureThreshold,
        "roomTemperatureLessGreaterThan" : roomTemperatureLessGreaterThan,
        "SQLLight" : mySQLLight, "SQLSoilMoisture" : mySQLSoilMoisture,
        "SQLRoomHumidity" : mySQLRoomHumidity, 
        "SQLRoomTemperature" : mySQLRoomTemperature}
        return newVariablesValues
    return


def setDefaultThresholds_noPotIDParameterTest():
    testInput = {"RoomID" : 2, "OwnerID": 1}
    expectedOutput = "potID not found"
    output = setDefaultThresholds(testInput)

    print("\n ****************************  Testing setDefaultThresholds() when potID not in parameter  ****************************")
    print("Input: ")
    print("\t" + str(testInput))
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print ("Received: %s" %output)
    return

def setDefaultThresholds_SetDefaultLightTest(): 
    potID = 1
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))

    testInput1  = {"potID" : str(potID), "RoomID" : str(2), "OwnerID": str(1)}
    testInput2 = {"lightThreshold" : "-",
    "lightLessGreaterThan" : "-",
    "soilMoistureThreshold" : "-",
    "soilMoistureLessGreaterThan" : "-",
    "roomHumidityThreshold" : "-", 
    "roomHumidityLessGreaterThan" : "-",
    "roomTemperatureThreshold" : "-",
    "roomTemperatureLessGreaterThan" : "-", "tdate" : tdate, "ttime" : ttime}
    expectedOuput = ["70", ">"]

    output = setDefaultThresholds(testInput1, testInput2)
    output = [str(output.get("lightThreshold")), str(output.get("lightLessGreaterThan")), str(output.get("SQLLight"))]


    print("\n ****************************  Testing setDefaultThresholds() for Setting Default Light Threshold Value ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tLight threshold value to be set to: " + str(expectedOuput[0]))  
    
    if expectedOuput[0] == output[0].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[0])

    print("\n ****************************  Testing setDefaultThresholds() for Setting Default Light lessGreaterThan String  ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tLight lessGreaterThan string to be set to: " + str(expectedOuput[1]))  
    
    if expectedOuput[1] == output[1].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[1])

    print("\n ****************************  Testing setDefaultThresholds() for Correct Set Default Light Argument to updateUserThresholdsTable() ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    expectedOuput = str({"potID" : str(potID), "sensorType" : "light", "thresholdValue" : "70", "lessGreaterThan" : ">","tdate" : tdate, "ttime" : ttime})
    print("Expected Ouput: ")
    print("\t" + expectedOuput)  
    
    if expectedOuput.replace(" ", "") == output[2].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[2])
    return
    
def setDefaultThresholds_SetDefaultSoilMoistureTest():
    potID = 1
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))

    testInput1  = {"potID" : 1, "RoomID" : 2, "OwnerID": 1}
    testInput2 = {"lightThreshold" : "-",
    "lightLessGreaterThan" : "-",
    "soilMoistureThreshold" : "-",
    "soilMoistureLessGreaterThan" : "-",
    "roomHumidityThreshold" : "-", 
    "roomHumidityLessGreaterThan" : "-",
    "roomTemperatureThreshold" : "-",
    "roomTemperatureLessGreaterThan" : "-", "tdate" : tdate, "ttime" : ttime}
    expectedOuput = ["70", ">"]

    output = setDefaultThresholds(testInput1, testInput2)
    output = [str(output.get("soilMoistureThreshold")), str(output.get("soilMoistureLessGreaterThan")), str(output.get("SQLSoilMoisture"))]


    print("\n ****************************  Testing setDefaultThresholds() for Setting Default Soil Moisture Threshold Value ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tSoil Moisture threshold value to be set to: " + str(expectedOuput[0]))  
    
    if expectedOuput[0] == output[0].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[0])

    print("\n ****************************  Testing setDefaultThresholds() for Setting Default Soil Moisture lessGreaterThan String  ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tSoil Moisture lessGreaterThan string to be set to: " + str(expectedOuput[1]))  
    
    if expectedOuput[1] == output[1].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[1])

    print("\n ****************************  Testing setDefaultThresholds() for Correct Set Default Soil Moisture Argument to updateUserThresholdsTable() ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    expectedOuput = str({"potID" : str(potID), "sensorType" : "soilMoisture", "thresholdValue" : "70", "lessGreaterThan" : ">", "tdate" : tdate, "ttime" : ttime})
    print("Expected Ouput: ")
    print("\t" + expectedOuput)  
    
    if expectedOuput.replace(" ", "") == output[2].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[2])
    return
    


def setDefaultThresholds_SetDefaultRoomHumidityTest():
    potID = 1
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))

    testInput1  = {"potID" : 1, "RoomID" : 2, "OwnerID": 1}
    testInput2 = {"lightThreshold" : "-",
    "lightLessGreaterThan" : "-",
    "soilMoistureThreshold" : "-",
    "soilMoistureLessGreaterThan" : "-",
    "roomHumidityThreshold" : "-", 
    "roomHumidityLessGreaterThan" : "-",
    "roomTemperatureThreshold" : "-",
    "roomTemperatureLessGreaterThan" : "-", "tdate" : tdate, "ttime" : ttime}
    expectedOuput = ["70", ">"]

    output = setDefaultThresholds(testInput1, testInput2)
    output = [str(output.get("roomHumidityThreshold")), str(output.get("roomHumidityLessGreaterThan")), str(output.get("SQLRoomHumidity"))]


    print("\n ****************************  Testing setDefaultThresholds() for Setting Default Room Humidity Threshold Value ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tRoom Humidity threshold value to be set to: " + str(expectedOuput[0]))  
    
    if expectedOuput[0] == output[0].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[0])

    print("\n ****************************  Testing setDefaultThresholds() for Setting Default Room Humidity lessGreaterThan String  ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tRoom Humidity lessGreaterThan string to be set to: " + str(expectedOuput[1]))  
    
    if expectedOuput[1] == output[1].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[1])
    
    print("\n ****************************  Testing setDefaultThresholds() for Correct Set Default Room Humidity Argument to updateUserThresholdsTable() ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    expectedOuput = str({"potID" : str(potID), "sensorType" : "roomHumidity", "thresholdValue" : "70", "lessGreaterThan" : ">", "tdate" : tdate, "ttime" : ttime})
    print("Expected Ouput: ")
    print("\t" + expectedOuput)  
    
    if expectedOuput.replace(" ", "") == output[2].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[2])
    return

def setDefaultThresholds_SetDefaultRoomTemperatureTest():
    potID = 1
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))

    testInput1  = {"potID" : 1, "RoomID" : 2, "OwnerID": 1}
    testInput2 = {"lightThreshold" : "-",
    "lightLessGreaterThan" : "-",
    "soilMoistureThreshold" : "-",
    "soilMoistureLessGreaterThan" : "-",
    "roomHumidityThreshold" : "-", 
    "roomHumidityLessGreaterThan" : "-",
    "roomTemperatureThreshold" : "-",
    "roomTemperatureLessGreaterThan" : "-", "tdate" : tdate, "ttime" : ttime}
    expectedOuput = ["70", ">"]

    output = setDefaultThresholds(testInput1, testInput2)
    output = [str(output.get("roomTemperatureThreshold")), str(output.get("roomTemperatureLessGreaterThan")), str(output.get("SQLRoomTemperature"))]


    print("\n ****************************  Testing setDefaultThresholds() for Setting Default Room Temperature Threshold Value ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tRoom Temperature threshold value to be set to: " + str(expectedOuput[0]))  
    
    if expectedOuput[0] == output[0].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[0])

    print("\n ****************************  Testing setDefaultThresholds() for Setting Default Room Temperature lessGreaterThan String  ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tRoom Temperature lessGreaterThan string to be set to: " + str(expectedOuput[1]))  
    
    if expectedOuput[1] == output[1].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[1])

    print("\n ****************************  Testing setDefaultThresholds() for Correct Set Default Room Temperature Argument to updateUserThresholdsTable() ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    expectedOuput = str({"potID" : str(potID), "sensorType" : "roomTemperature", "thresholdValue" : "70", "lessGreaterThan" : ">", "tdate" : tdate, "ttime" : ttime})
    print("Expected Ouput: ")
    print("\t" + expectedOuput)  
    
    if expectedOuput.replace(" ", "") == output[2].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[2])
    return
          
          
setDefaultThresholds_noPotIDParameterTest()
input("")
setDefaultThresholds_SetDefaultLightTest()
input("")
setDefaultThresholds_SetDefaultSoilMoistureTest()
input("")
setDefaultThresholds_SetDefaultRoomHumidityTest()
input("")
setDefaultThresholds_SetDefaultRoomTemperatureTest()
