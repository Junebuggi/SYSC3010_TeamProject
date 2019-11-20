#Author: Abeer Rafiq
#Last Modified: November, 20, 2019

import time, json
from datetime import datetime, date

def updateUserThresholdsTable(threshold, testingInput=None):
    global cursor, dbconnect
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
                
    if "potID" not in threshold.keys():
        return "potID not found"
    if "lessGreaterThan" not in threshold.keys():
        return "lessGreaterThan not found"
    if "sensorType" not in threshold.keys():
        return "sensorType not found"
    if "thresholdValue" not in threshold.keys():
        return "thresholdValue not found"
    if "tdate" not in threshold.keys():
        return "tdate not found"
    if "ttime" not in threshold.keys():
        return "ttime not found"
        
    potID = threshold.get("potID")
    lessGreaterThan = threshold.get("lessGreaterThan")
    thresholdValue = threshold.get("thresholdValue")
    sensorType = threshold.get("sensorType")
    tdate = threshold.get("tdate")
    ttime = threshold.get("ttime")
   
    mySQL = "insert into userThresholds values ('" + str(potID) + "', '" + str(sensorType) + "', '" + str(thresholdValue) + "', '" + str(lessGreaterThan) + "', '" + str(tdate) + "', '" + str(ttime) + "')"    
    if testingInput is None:
        cursor.execute(mySQL)
        dbconnect.commit();
  
    if sensorType == "light":
        lightThreshold = str(thresholdValue)
        lightLessGreaterThan = str(lessGreaterThan)
    elif sensorType == "soilMoisture":
        soilMoistureThreshold = str(thresholdValue)
        soilMoistureLessGreaterThan = str(lessGreaterThan)
    elif sensorType == "roomTemperature":
        roomTemperatureThreshold = str(thresholdValue)
        roomTemperatureLessGreaterThan = str(lessGreaterThan)
    elif sensorType == "roomHumidity":
        roomHumidityThreshold = str(thresholdValue)
        roomHumidityLessGreaterThan = str(lessGreaterThan)

    if testingInput != None:
        newVariablesValues = {"mySQL" : mySQL, "lightThreshold" : lightThreshold,
        "lightLessGreaterThan" : lightLessGreaterThan,
        "soilMoistureThreshold" : soilMoistureThreshold,
        "soilMoistureLessGreaterThan" : soilMoistureLessGreaterThan,
        "roomHumidityThreshold" : roomHumidityThreshold, 
        "roomHumidityLessGreaterThan" : roomHumidityLessGreaterThan,
        "roomTemperatureThreshold" : roomTemperatureThreshold,
        "roomTemperatureLessGreaterThan" : roomTemperatureLessGreaterThan}
        return newVariablesValues
    return

def updateUserThresholdsTable_noPotIDParameterTest():
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    testInput = {"sensorType" : "light", "lessGreaterThan" : "<", "thresholdValue" : 50, "ttime" : ttime, "tdate" : tdate}
    expectedOutput = "potID not found"
    output = updateUserThresholdsTable(testInput)

    print("\n ****************************  Testing updateUserThresholdsTable() when potID not in parameter  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: " + output)	
    return
    
def updateUserThresholdsTable_noTDateParameterTest():
    testInput = {"sensorType" : "light", "lessGreaterThan" : "<", "thresholdValue" : 50, "potID" : 1, "ttime" : str(datetime.now().strftime("%H:%M:%S"))}
    expectedOutput = "tdate not found"
    output = updateUserThresholdsTable(testInput)

    print("\n ****************************  Testing updateUserThresholdsTable() when tdate not in parameter  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: " + output)	
    return

def updateUserThresholdsTable_noTTimeParameterTest():
    testInput = {"sensorType" : "light", "lessGreaterThan" : "<", "thresholdValue" : 50, "potID" : 1, "tdate" : str(date.today())}
    expectedOutput = "ttime not found"
    output = updateUserThresholdsTable(testInput)

    print("\n ****************************  Testing updateUserThresholdsTable() when ttime not in parameter  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: " + output)	
    return
    
def updateUserThresholdsTable_noThresholdValueParameterTest():
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    testInput = {"sensorType" : "light", "lessGreaterThan" : "<", "potID": 1, "ttime" : ttime, "tdate" : tdate}
    expectedOutput = "thresholdValue not found"
    output = updateUserThresholdsTable(testInput)

    print("\n ****************************  Testing updateUserThresholdsTable() when thresholdValue not in parameter  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: " + output)	
    return

def updateUserThresholdsTable_noSensorTypeParameterTest():
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    testInput = {"potID" : 1, "lessGreaterThan" : "<", "thresholdValue" : 50, "ttime" : ttime, "tdate" : tdate}
    expectedOutput = "sensorType not found"
    output = updateUserThresholdsTable(testInput)

    print("\n ****************************  Testing updateUserThresholdsTable() when sensorType not in parameter  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: " + output)	
    return


def updateUserThresholdsTable_noLessGreaterThanParameterTest():
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    testInput = {"potID" : 1, "sensorType" : "light", "thresholdValue" : 50, "ttime" : ttime, "tdate" : tdate}
    expectedOutput = "lessGreaterThan not found"
    output = updateUserThresholdsTable(testInput)

    print("\n ****************************  Testing updateUserThresholdsTable() when lessGreaterThan not in parameter  ****************************")
    print("Input: ")
    for key in testInput:
        print("\t" + key + " = " + str(testInput[key]))  
    print("Expected Ouput: \n\t%s" % expectedOutput)
    if output.replace(" ", "") == expectedOutput.replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: " + output)	
    return


def updateUserThresholdsTable_SQLInsertTest():
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    
    testInput1 = {"potID" : "1",  "sensorType" : "light",  "thresholdValue" : 50, "lessGreaterThan" : "<","tdate" : tdate, "ttime" : ttime}
    testInput2 = {"lightThreshold" : "50",
    "lightLessGreaterThan" : "<",
    "soilMoistureThreshold" : "50",
    "soilMoistureLessGreaterThan" : "<",
    "roomHumidityThreshold" : "50", 
    "roomHumidityLessGreaterThan" : "<",
    "roomTemperatureThreshold" : "50",
    "roomTemperatureLessGreaterThan" : "<"}
    
    expectedSQL = "insert into userThresholds values ('1', 'light', '50', '<', '" + str(tdate) + "', '" + str(ttime) + "')" 
    output = updateUserThresholdsTable(testInput1, testInput2)

    print("\n ****************************  Testing updateUserThresholdsTable() for Right SQL Statement  ****************************")
    print("Input: ")
    print("\t" + str(testInput1))  
    print("Expected Ouput: ")
    print("\t" + str(expectedSQL))  
    if str(expectedSQL).replace(" ", "") == str(output.get("mySQL")).replace(" ", ""):
        print ("Result: PASS	")
    else:
        print ("Result: FAIL")
        print("Received: " + output)	
    return
    
def updateUserThresholdsTable_SetRoomTemperatureThresholdsTest():
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    
    testInput1 = {"potID" : "1",  "sensorType" : "roomTemperature",  "thresholdValue" : 80, "lessGreaterThan" : ">","tdate" : tdate, "ttime" : ttime}
    testInput2 = {"lightThreshold" : "50",
    "lightLessGreaterThan" : "<",
    "soilMoistureThreshold" : "50",
    "soilMoistureLessGreaterThan" : "<",
    "roomHumidityThreshold" : "50", 
    "roomHumidityLessGreaterThan" : "<",
    "roomTemperatureThreshold" : "50",
    "roomTemperatureLessGreaterThan" : "<"}
    expectedOuput = ["80", ">"]
    
    output = updateUserThresholdsTable(testInput1, testInput2)
    output = [str(output.get("roomTemperatureThreshold")), str(output.get("roomTemperatureLessGreaterThan"))]

    print("\n ****************************  Testing updateUserThresholdsTable() for Setting Room Temperature Threshold Value ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tRoom temperature threshold value to be set to: " + str(expectedOuput[0]))  
    
    if expectedOuput[0] == output[0].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[0])

    print("\n ****************************  Testing updateUserThresholdsTable() for Setting Room Temperature lessGreaterThan String  ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tRoom temperature lessGreaterThan string to be set to: " + str(expectedOuput[1]))  
    
    if expectedOuput[1] == output[1].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[1])
    return



def updateUserThresholdsTable_SetSoilMoistureThresholdsTest():
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    
    testInput1 = {"potID" : "1",  "sensorType" : "soilMoisture",  "thresholdValue" : 80, "lessGreaterThan" : ">","tdate" : tdate, "ttime" : ttime}
    testInput2 = {"lightThreshold" : "50",
    "lightLessGreaterThan" : "<",
    "soilMoistureThreshold" : "50",
    "soilMoistureLessGreaterThan" : "<",
    "roomHumidityThreshold" : "50", 
    "roomHumidityLessGreaterThan" : "<",
    "roomTemperatureThreshold" : "50",
    "roomTemperatureLessGreaterThan" : "<"}
    expectedOuput = ["80", ">"]

    output = updateUserThresholdsTable(testInput1, testInput2)
    output = [str(output.get("soilMoistureThreshold")), str(output.get("soilMoistureLessGreaterThan"))]

    print("\n ****************************  Testing updateUserThresholdsTable() for Setting Soil Moisture Threshold Value ****************************")
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

    print("\n ****************************  Testing updateUserThresholdsTable() for Setting Soil Moisture lessGreaterThan String  ****************************")
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
    return



def updateUserThresholdsTable_SetRoomHumidityThresholdsTest():
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    
    testInput1 = {"potID" : "1",  "sensorType" : "roomHumidity",  "thresholdValue" : 80, "lessGreaterThan" : ">","tdate" : tdate, "ttime" : ttime}
    testInput2 = {"lightThreshold" : "50",
    "lightLessGreaterThan" : "<",
    "soilMoistureThreshold" : "50",
    "soilMoistureLessGreaterThan" : "<",
    "roomHumidityThreshold" : "50", 
    "roomHumidityLessGreaterThan" : "<",
    "roomTemperatureThreshold" : "50",
    "roomTemperatureLessGreaterThan" : "<"}
    expectedOuput = ["80", ">"]

    output = updateUserThresholdsTable(testInput1, testInput2)
    output = [str(output.get("roomHumidityThreshold")), str(output.get("roomHumidityLessGreaterThan"))]


    print("\n ****************************  Testing updateUserThresholdsTable() for Setting Room humidity Threshold Value ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tRoom humidity threshold value to be set to: " + str(expectedOuput[0]))  
    
    if expectedOuput[0] == output[0].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[0])

    print("\n ****************************  Testing updateUserThresholdsTable() for Setting Room humidity lessGreaterThan String  ****************************")
    print("Input 1: ")
    print("\t" + str(testInput1))
    print("Input 2: ")
    for key in testInput2:
        print("\t" + key + " = " + str(testInput2[key]))  

    print("Expected Ouput: ")
    print("\tRoom humidity lessGreaterThan string to be set to: " + str(expectedOuput[1]))  
    
    if expectedOuput[1] == output[1].replace(" ", ""):
        print ("Result: PASS")
    else:
        print ("Result: FAIL")
        print("Received: %s" %output[1])
    return


def updateUserThresholdsTable_SetLightThresholdsTest():
    tdate = str(date.today())
    ttime = str(datetime.now().strftime("%H:%M:%S"))
    
    testInput1 = {"potID" : "1",  "sensorType" : "light",  "thresholdValue" : 80, "lessGreaterThan" : ">","tdate" : tdate, "ttime" : ttime}
    testInput2 = {"lightThreshold" : "50",
    "lightLessGreaterThan" : "<",
    "soilMoistureThreshold" : "50",
    "soilMoistureLessGreaterThan" : "<",
    "roomHumidityThreshold" : "50", 
    "roomHumidityLessGreaterThan" : "<",
    "roomTemperatureThreshold" : "50",
    "roomTemperatureLessGreaterThan" : "<"}
    expectedOuput = ["80", ">"]

    output = updateUserThresholdsTable(testInput1, testInput2)
    output = [str(output.get("lightThreshold")), str(output.get("lightLessGreaterThan"))]


    print("\n ****************************  Testing updateUserThresholdsTable() for Setting Light Threshold Value ****************************")
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

    print("\n ****************************  Testing updateUserThresholdsTable() for Setting Light lessGreaterThan String  ****************************")
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
    return

updateUserThresholdsTable_noPotIDParameterTest()
input("")
updateUserThresholdsTable_noTDateParameterTest()
input("")
updateUserThresholdsTable_noTTimeParameterTest()
input("")
updateUserThresholdsTable_noThresholdValueParameterTest()
input("")
updateUserThresholdsTable_noLessGreaterThanParameterTest()
input("")
updateUserThresholdsTable_noSensorTypeParameterTest()
input("")
updateUserThresholdsTable_SQLInsertTest()
input("")
updateUserThresholdsTable_SetLightThresholdsTest()
input("")
updateUserThresholdsTable_SetRoomHumidityThresholdsTest()
input("")
updateUserThresholdsTable_SetRoomTemperatureThresholdsTest()
input("")
updateUserThresholdsTable_SetSoilMoistureThresholdsTest()
