EESchema Schematic File Version 4
LIBS:RPi_Sensor_Schematic-cache
EELAYER 30 0
EELAYER END
$Descr User 8909 6299
encoding utf-8
Sheet 1 1
Title "The Plant Nursery's Raspberry Pi Sensors"
Date "2019-10-18"
Rev "2"
Comp "Carleton University TeamW4"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 5DA72366
P 1800 2850
F 0 "J1" H 1800 4450 50  0000 C CNN
F 1 "Raspberry_Pi_4" H 1800 4350 50  0000 C CNN
F 2 "" H 1800 2850 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 1800 2850 50  0001 C CNN
	1    1800 2850
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 5DA8AD2A
P 3350 2750
F 0 "R1" H 3420 2796 50  0000 L CNN
F 1 "10KΩ" H 3420 2705 50  0000 L CNN
F 2 "" V 3280 2750 50  0001 C CNN
F 3 "~" H 3350 2750 50  0001 C CNN
	1    3350 2750
	1    0    0    -1  
$EndComp
$Comp
L TeamW4:DHT22 U1
U 1 1 5DA8D139
P 3900 2750
F 0 "U1" H 4130 2796 50  0000 L CNN
F 1 "DHT22" H 4130 2705 50  0000 L CNN
F 2 "Sensor:Aosong_DHT11_5.5x12.0_P2.54mm" H 3900 2350 50  0001 C CNN
F 3 "http://akizukidenshi.com/download/ds/aosong/DHT11.pdf" H 4050 3000 50  0001 C CNN
	1    3900 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3800 3050 3350 3050
Wire Wire Line
	3350 2900 3350 3050
Wire Wire Line
	3900 2450 3900 2350
Wire Wire Line
	3900 2350 3350 2350
Wire Wire Line
	3350 2350 3350 2600
Wire Wire Line
	1700 1550 1700 1450
Wire Wire Line
	2100 4150 2100 4350
Wire Wire Line
	2100 4350 3900 4350
Wire Wire Line
	3900 4350 3900 3050
Wire Wire Line
	3350 3050 3100 3050
Wire Wire Line
	3100 3050 3100 2550
Wire Wire Line
	3100 2550 2600 2550
Connection ~ 3350 3050
$Comp
L TeamW4:I2C_LCD_MODEL_V1.2 U2
U 1 1 5DA92B88
P 5100 2150
F 0 "U2" H 6078 1621 50  0000 L CNN
F 1 "I2C_LCD_MODEL_V1.2" H 6078 1530 50  0000 L CNN
F 2 "" H 4650 2200 50  0001 C CNN
F 3 "" H 4650 2200 50  0001 C CNN
	1    5100 2150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5450 3200 5450 4350
Wire Wire Line
	5450 4350 3900 4350
Connection ~ 3900 4350
Wire Wire Line
	5450 2250 5450 1450
Wire Wire Line
	5000 2800 4800 2800
Wire Wire Line
	4800 2800 4800 2050
Wire Wire Line
	4800 2050 2900 2050
Wire Wire Line
	2900 2050 2900 2350
Wire Wire Line
	2900 2350 2600 2350
Wire Wire Line
	5000 2900 4500 2900
Wire Wire Line
	4500 2900 4500 3200
Wire Wire Line
	4500 3200 2800 3200
Wire Wire Line
	2800 3200 2800 2250
Wire Wire Line
	2800 2250 2600 2250
$Comp
L Device:R R2
U 1 1 5DA94F25
P 7250 3050
F 0 "R2" H 7320 3096 50  0000 L CNN
F 1 "330Ω" H 7320 3005 50  0000 L CNN
F 2 "" V 7180 3050 50  0001 C CNN
F 3 "~" H 7250 3050 50  0001 C CNN
	1    7250 3050
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D1
U 1 1 5DA95AFF
P 7250 2500
F 0 "D1" V 7197 2578 50  0000 L CNN
F 1 "LED" V 7288 2578 50  0000 L CNN
F 2 "" H 7250 2500 50  0001 C CNN
F 3 "~" H 7250 2500 50  0001 C CNN
	1    7250 2500
	0    1    1    0   
$EndComp
Wire Wire Line
	7250 2900 7250 2650
Wire Wire Line
	7250 3200 7250 4350
Wire Wire Line
	7250 4350 5450 4350
Connection ~ 5450 4350
Wire Wire Line
	7250 2350 7250 1100
Wire Wire Line
	7250 1100 850  1100
Wire Wire Line
	850  1100 850  2450
Wire Wire Line
	850  2450 1000 2450
Text Notes 5550 2250 0    50   ~ 10
16x2 LCD Display\n
Text Notes 7500 2450 0    50   ~ 10
Detecting Measurements\nDebugging \nRED LED
Text Notes 7500 2800 0    50   ~ 0
Blinks when there is\nan error when reading\nmeasurements
Connection ~ 3900 1450
Connection ~ 3900 2350
Wire Wire Line
	5450 1450 3900 1450
Wire Wire Line
	1700 1450 3900 1450
Text Notes 3400 2300 0    50   ~ 10
Humidity and Temperature Sensor\n
Wire Wire Line
	3900 1450 3900 2350
$Comp
L Device:R R3
U 1 1 5DB5764F
P 8700 3050
F 0 "R3" H 8770 3096 50  0000 L CNN
F 1 "330Ω" H 8770 3005 50  0000 L CNN
F 2 "" V 8630 3050 50  0001 C CNN
F 3 "~" H 8700 3050 50  0001 C CNN
	1    8700 3050
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D2
U 1 1 5DB57655
P 8700 2500
F 0 "D2" V 8647 2578 50  0000 L CNN
F 1 "LED" V 8738 2578 50  0000 L CNN
F 2 "" H 8700 2500 50  0001 C CNN
F 3 "~" H 8700 2500 50  0001 C CNN
	1    8700 2500
	0    1    1    0   
$EndComp
Wire Wire Line
	8700 2900 8700 2650
Wire Wire Line
	8700 3200 8700 4350
Wire Wire Line
	8700 2350 8700 1100
Text Notes 8950 2450 0    50   ~ 10
Receiving Data\nDebugging \nGREEN LED
Text Notes 8950 2800 0    50   ~ 0
Blinks when receiving\ndata from arduino
$Comp
L Device:R R4
U 1 1 5DB588E9
P 10050 3050
F 0 "R4" H 10120 3096 50  0000 L CNN
F 1 "330Ω" H 10120 3005 50  0000 L CNN
F 2 "" V 9980 3050 50  0001 C CNN
F 3 "~" H 10050 3050 50  0001 C CNN
	1    10050 3050
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D3
U 1 1 5DB588EF
P 10050 2500
F 0 "D3" V 9997 2578 50  0000 L CNN
F 1 "LED" V 10088 2578 50  0000 L CNN
F 2 "" H 10050 2500 50  0001 C CNN
F 3 "~" H 10050 2500 50  0001 C CNN
	1    10050 2500
	0    1    1    0   
$EndComp
Wire Wire Line
	10050 2900 10050 2650
Wire Wire Line
	10050 3200 10050 4350
Wire Wire Line
	10050 2350 10050 1100
Text Notes 10300 2450 0    50   ~ 10
Receiving Data\nDebugging \nBLUE LED
Text Notes 10300 2800 0    50   ~ 0
Blinks when receiving\ndata from arduino
Wire Wire Line
	8700 1100 7250 1100
Connection ~ 7250 1100
Wire Wire Line
	8700 4350 7250 4350
Connection ~ 7250 4350
Wire Wire Line
	10200 4350 10050 4350
Connection ~ 8700 4350
Wire Wire Line
	10200 1100 10050 1100
Connection ~ 8700 1100
Connection ~ 10050 1100
Wire Wire Line
	10050 1100 8700 1100
Connection ~ 10050 4350
Wire Wire Line
	10050 4350 8700 4350
$EndSCHEMATC
