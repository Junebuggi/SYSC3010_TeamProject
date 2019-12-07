# SYSC3010_TeamProject: The Plant Nursery :sparkles: :seedling:
Completed on: 06/12/19 

SYSC 3010 The Plant Nursery Project Repository 

							The Plant Nursery 
					An automated plant watering and monitoring system				
<p align="center">
<img src="https://github.com/Junebuggi/SYSC3010_TeamW4/blob/master/logo.jpg" width="400">
</p>

Contributors:
--------------

Ruqaya Almalki\
Emma Boulay\
Abeer Rafiq\
Abdul-Rahmaan Rufai

------------------------------------------------------------------------------------------------------------------------------
To operate this system in a similar fashion as we have done, you will require 2 Raspberry pi's, an Arduino, an Android smart phone and an internet connection. All python scripts have been developed using the Python 2.7 language. You will need to find the IP of each Pi by using the ifconfig command in the terminal. Replace the IP in the app, roomPi and globalServer scripts to reflect this.

Additional Hardware used:

* Capacitive Soil Moisture Sensor

* Light Dependent Resistor

* Ultrasonic Sensor

* Temperature and Humidity Sensor

* DC Water Pump

* 5V Relay Module (active low) 

* 16x2 LCD 

How to Set-up the globalServer Raspberry Pi
--------------------------

1.Open Terminal and run the following commands:

	pi@raspberry:~ $ sudo apt update
	
	pi@raspberry:~ $ sudo apt-get install sqlite3

2.To create the Database and the tables run the following commands in the terminal

	pi@raspberry:~ $ sqlite3 PlantNursery.db
	
	sqlite> BEGIN;
	
	sqlite> CREATE TABLE `potData` ( `potID` INTEGER, `light` REAL, `soilMoisture` REAL, `waterDistance` REAL, `tdate` DATE, `ttime` TIME )
	
	sqlite> CREATE TABLE `roomData` ( `roomID` INTEGER, `temperature` REAL, `humidity` REAL, `tdate` DATE, `ttime` TIME )
	
	sqlite> CREATE TABLE "userNotes" ( `potID` INTEGER, `notes` TEXT, `tdate` DATE, `ttime` TIME )
	
	sqlite> CREATE TABLE `userPlants` ( `roomID` INTEGER, `potID` INTEGER, `ownerID` INTEGER )

	sqlite> CREATE TABLE `userThresholds` ( `potID` INTEGER, `sensorType` TEXT, `thresholdValue` REAL, `lessGreaterThan` TEXT, `tdate` DATE, `ttime` TIME )
	
	sqlite> COMMIT;
	
3.Download globalServer folder\
4.Unzip contents to Desktop\
5.Open both globalServerApp.py and globalServerRoomPi.py\
6.In the globalServerApp.py file, go to line 295 and change the second parameter to the phone's IP address <br />
7.In the globalServerRoomPi.py, go to line 346 and input the phone's IP address as the 4rth parameter
and the roomPi's IP address as the 3rd parameter\
8.Navigate to the Desktop

	pi@raspberry:~ $ cd \Desktop
	
9.Run the shell command to start the globalServerApp.py and the globalServerRoomPi.py scripts

	pi@raspberry:~ $ sudo sh globalServer.sh


How to Set-up the RoomPi Raspberry Pi
--------------------------

1.Connect the hardware to the Raspberry Pi following the roomPi schematic
1.Download roomPi folder\
2.Unzip contents to Desktop\
3.Go to line 327 in the roomPiManger.py file and change the second parameter to the Global Pi's IP address

4.Navigate to the Desktop

	pi@raspberry:~ $ cd \Desktop
	
5.Open the terminal and run the following command:

	pi@raspberry:~ $ sudo python roomPiManager.py
	

How to Set-up the potSensors Arduino
--------------------------
1.Connect the hardware to the Arduino following the potSensors Arduino schematic
2.Plug Arduino into roomPi Raspberry Pi using a USB cable\
3.Open Terminal and run the following commands:

	pi@raspberry:~ $ sudo apt-get update
	
	pi@raspberry:~ $ sudo apt-get install arduino
	
4.Download potSensorsManager
5.Unzip contents to Desktop\
6.Navigate to potSensorsManager -> potSensorsManager.ino and open using the Arduino IDE\
7.On the top left of the Arduino IDE click the forward arrow "Upload"

How to Set-up the Plant Nursery Android Application
--------------------------
1.Install Android Studio.\
2.Download the Android_App folder in the clean version\
3.Open Android Studio and navigate to the Android_App folder\
4.Run the app.\
5.It can be ran either using the emulator or an android phone\
6.Please note you may need to modify the code dependent on the ipaddress and the port to be sent to.
