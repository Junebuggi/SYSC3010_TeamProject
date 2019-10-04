/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman
  modified 25 September 2019
  By Team W4: Carleton University

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Blink
*/

// the setup function runs once when you press reset or power the board
#include <MsTimer2.h>
#define var_resistor A0

int var_resistor_value ; //Global Variable

void readVariableResistor (); 
 
void setup() {
 // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin (115200);
  MsTimer2::set (20 , readVariableResistor ); 
  MsTimer2::start (); 
}

// the loop function runs over and over again forever
void loop() {
  
  var_resistor_value = analogRead( var_resistor );
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(var_resistor_value);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(var_resistor_value);                       // wait for a second
}

void readVariableResistor (){ // read the analog input from the variable resistor
  var_resistor_value = analogRead( var_resistor );
  // Send the value over serial COM port 
  Serial.println ( var_resistor_value ); 
}
