EESchema Schematic File Version 4
LIBS:RPi_Sensor_Schematic-cache
EELAYER 30 0
EELAYER END
$Descr User 10024 7087
encoding utf-8
Sheet 1 1
Title "The Plant Nursery's Raspberry Pi Server"
Date "2019-10-18"
Rev "1"
Comp "Carleton University TeamW4"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	3350 1900 3350 1950
$Comp
L Device:R R1
U 1 1 5DAA6C98
P 5250 3450
F 0 "R1" H 5320 3496 50  0000 L CNN
F 1 "330Ω" H 5320 3405 50  0000 L CNN
F 2 "" V 5180 3450 50  0001 C CNN
F 3 "~" H 5250 3450 50  0001 C CNN
	1    5250 3450
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D1
U 1 1 5DAA7AAC
P 5250 2750
F 0 "D1" V 5197 2828 50  0000 L CNN
F 1 "LED" V 5288 2828 50  0000 L CNN
F 2 "" H 5250 2750 50  0001 C CNN
F 3 "~" H 5250 2750 50  0001 C CNN
	1    5250 2750
	0    1    1    0   
$EndComp
Wire Wire Line
	5250 3300 5250 2900
Wire Wire Line
	3850 4550 3850 4700
Wire Wire Line
	3850 4700 5250 4700
Wire Wire Line
	5250 4700 5250 3600
Connection ~ 5250 4700
Wire Wire Line
	5250 2600 5250 1650
Wire Wire Line
	2550 2850 2750 2850
Wire Wire Line
	4850 2100 4850 3950
Wire Wire Line
	4850 3950 4350 3950
Text Notes 5300 2550 0    50   ~ 10
RPI UDP Transmission\nDebugging LED
Wire Wire Line
	6750 2600 6750 2100
Wire Wire Line
	6750 2900 6750 3300
Wire Wire Line
	6750 4700 6750 3600
$Comp
L Device:LED D2
U 1 1 5DAABAEB
P 6750 2750
F 0 "D2" V 6697 2828 50  0000 L CNN
F 1 "LED" V 6788 2828 50  0000 L CNN
F 2 "" H 6750 2750 50  0001 C CNN
F 3 "~" H 6750 2750 50  0001 C CNN
	1    6750 2750
	0    1    1    0   
$EndComp
$Comp
L Device:R R2
U 1 1 5DAABAE5
P 6750 3450
F 0 "R2" H 6820 3496 50  0000 L CNN
F 1 "330Ω" H 6820 3405 50  0000 L CNN
F 2 "" V 6680 3450 50  0001 C CNN
F 3 "~" H 6750 3450 50  0001 C CNN
	1    6750 3450
	1    0    0    -1  
$EndComp
Text Notes 5350 3050 0    50   ~ 0
Blinks when receiving \ndata from roomRPI
Text Notes 6800 2550 0    50   ~ 10
Android App UDP Transmission\nDebugging LED
Text Notes 6850 3050 0    50   ~ 0
Blinks when receiving \ndata from plantNannyApp
Wire Wire Line
	4850 2100 6750 2100
Wire Wire Line
	5250 4700 6750 4700
Text Notes 2250 2000 0    59   ~ 12
plantNannyServer
Wire Wire Line
	2550 1650 2550 2850
Wire Wire Line
	5250 1650 2550 1650
$Comp
L RPi_Sensor_Schematic-rescue:Raspberry_Pi_2_3-Connector J1
U 1 1 5DA72366
P 3550 3250
F 0 "J1" H 3550 4731 50  0000 C CNN
F 1 "Raspberry_Pi_4" H 3550 4640 50  0000 C CNN
F 2 "" H 3550 3250 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 3550 3250 50  0001 C CNN
	1    3550 3250
	1    0    0    -1  
$EndComp
$EndSCHEMATC
