EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:ESP8266
LIBS:AMS1117
LIBS:SparkFun
LIBS:esp-adapter-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L AMS1117 U?
U 1 1 5771351A
P 2600 1050
F 0 "U?" H 2600 950 50  0000 C CNN
F 1 "AMS1117" H 2600 1150 50  0000 C CNN
F 2 "" H 2600 1050 60  0000 C CNN
F 3 "" H 2600 1050 60  0000 C CNN
	1    2600 1050
	1    0    0    -1  
$EndComp
$Comp
L M06POGOPIN_HOLES_ONLY JP?
U 1 1 57713875
P 1050 2300
F 0 "JP?" H 850 2730 50  0000 L BNN
F 1 "M06POGOPIN_HOLES_ONLY" H 850 1900 50  0000 L BNN
F 2 "SparkFun-1X06_HOLES_ONLY" H 1050 2450 50  0001 C CNN
F 3 "" H 1050 2300 60  0000 C CNN
	1    1050 2300
	1    0    0    -1  
$EndComp
$Comp
L ESP-01v090 U?
U 1 1 57713C14
P 3900 2350
F 0 "U?" H 3900 2250 50  0000 C CNN
F 1 "ESP-01v090" H 3900 2450 50  0000 C CNN
F 2 "" H 3900 2350 50  0001 C CNN
F 3 "" H 3900 2350 50  0001 C CNN
	1    3900 2350
	1    0    0    -1  
$EndComp
Wire Wire Line
	1250 2500 2650 2500
Wire Wire Line
	2650 2500 2650 1900
Wire Wire Line
	2600 1900 4850 1900
Wire Wire Line
	4850 1900 4850 2200
Wire Wire Line
	2600 1550 2600 1900
Connection ~ 2650 1900
Wire Wire Line
	3400 1050 3400 1700
Wire Wire Line
	3400 1700 2750 1700
Wire Wire Line
	2750 1700 2750 2500
Wire Wire Line
	2750 2500 2950 2500
Wire Wire Line
	1250 2300 1800 2300
Wire Wire Line
	1800 2300 1800 1050
NoConn ~ 2000 2250
$EndSCHEMATC
