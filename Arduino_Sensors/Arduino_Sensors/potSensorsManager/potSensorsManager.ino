#define serialPi Serial
// #include <ArduinoJson.h>

const float criticalDistance = 20;

float initialDistance;
//Declare constant variables
const int potID = 1;
const double ldrLower = 390; //the value when the LDR is complete darkness
const double ldrUpper = 685; //the value when the LDR is in complete brightness
const double ldrRange = ldrUpper-ldrLower;
const int waitFor = 10; //the number of seconds to wait for. A multiple of 5 to avoid race conditions. 

//Declare Sensor and Pump Pins
const int ldrPin = A0;
const int trigPin = 10;
const int echoPin = 9;
const int soilMoisturePin = A2;
const int pumpPin = 7;

//Declare debugging LED pins
const int ldrLED = 13;
const int distanceLED = 11;
const int soilMoistureLED = 8; 
const int pumpLED = 6;

// Define sensor variables
int ldrValue;
long duration;
float distance;
int sensorValue;  

//Receiving Acknowledgments variables
String opcode = "";
String packetRec = "";
String packet;
int nPacket = 0;
int timerIterations;
int timer1_counter;
boolean resendPacket = false;


//Debugging LED statuses
boolean waterDistanceStatus;
boolean ldrStatus;
boolean soilMoistureStatus;
boolean waterPumpStatus;

String waterPumpDuration;
int seconds = 0;
int secondsB = 0;

//Function prototypes
void getLDR(void);
void getWaterLevel(void);
void getSoilMoisture(void);
void waterPumpManager(void);
void setup() {

  pinMode(ldrLED, OUTPUT);
  pinMode(distanceLED, OUTPUT);
  pinMode(soilMoistureLED, OUTPUT);
  pinMode(pumpLED, OUTPUT);
  pinMode(pumpPin, OUTPUT);
  
  //Set the sensor pins
  pinMode(ldrPin, INPUT);
  pinMode(soilMoisturePin, INPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

// // initialize timer1 
//  noInterrupts();           // disable all interrupts
//  TCCR1A = 0;
//  TCCR1B = 0;
//
//  // Set timer1_counter to the correct value for our interrupt interval
//  timer1_counter = 3124; 
//  TCNT1 = timer1_counter;   // preload timer
//  // Set CS11 bit for 8 prescaler
//  TCCR1B |= (1 << CS12) | (1 << CS10);  
////initialize timer2
//  TCCR2A = 0;
//  TCCR2B = 0;
//
//  // Set timer1_counter to the correct value for our interrupt interval
//  //timer2_counter = 3124; 
//  //TCNT2 = timer2_counter;   // preload timer
//  // Set CS11 bit for 8 prescaler
//  TCCR2B |= (1 << CS12) | (1 << CS10);  
//  interrupts();
//  TIMSK1 &= ~(1 << TOIE1); //Disable timer1 interrupts
//  TIMSK2 &= ~(1 << TOIE1); //Disable timer2 interrupts

 // initialize timer1 
 cli(); // disable global interrupts
TCCR1A = 0; // set entire TCCR1A register to 0
TCCR1B = 0; // same for TCCR1B

// set compare match register to desired timer count:
OCR1A = 15624;
// turn on CTC mode:
TCCR1B |= (1 << WGM12);
// Set CS10 and CS12 bits for 1024 prescaler:
TCCR1B |= (1 << CS10);
TCCR1B |= (1 << CS12);
// enable timer compare interrupt:
TIMSK1 |= (1 << OCIE1A);
// enable global interrupts:
sei();

TIMSK1 &= ~(1 << OCIE1A);



  serialPi.begin(9600); //begin serial on port 9600

}

void loop() {
  packet = "{\"opcode\": 8, \"potID\": " + String(potID);
  packet += ",";

  waterPumpManager();
  getWaterLevel();
  getLDR();
  getSoilMoisture();
  packet += "}";
  serialPi.println(packet);
  int startSend = millis();
  boolean noAckRec = true;
  while(millis() < startSend + 10000){ 
//    if(serialPi.available() > 0 && serialPi.peek() == '0' && noAckRec){ // Don't read unless there is data 
//      String ack = serialPi.readStringUntil('\n');
//      serialPi.println(packet);
//      noAckRec = false;
//    }
  }
 


//  //Timer1.attachInterrupt(timerIsr); // attach the service routine here
//  TIMSK1 |= (1 << TOIE1);
//  while((TIMSK1 & (1 << TOIE1))){ //Once the interrupt is disabled, continue with regular loop
//    if(resendPacket){
//      serialPi.println(packet);
//      resendPacket = false;
//    }
  //} 
  
  //delay((waitFor - (timerIterations * 5)) * 1000); //waitFor the remaining time left in the delay
  //nPacket = (nPacket + 1) % 100;
  
  
}

void waterPumpManager(void){
  
  waterPumpStatus = true;
  //write if for if there is enough water in the tank
//  if(abs(distance - criticalDistance) <= 0.01 && TIMSK2 & (1 << TOIE1)){ //Turn pump off and disable the interrupt if there is not enough water
//    digitalWrite(pumpPin, LOW); 
//    TIMSK2 &= ~(1 << TOIE1);   
 // }
  if(serialPi.available() > 0 && serialPi.peek() == 'C' ){ // Don't read unless there is data and its the startWaterPump opcode
    digitalWrite(pumpPin, HIGH);
    seconds = 0;
    //digitalWrite(soilMoistureLED, !digitalRead(soilMoistureLED));
    String opcode = serialPi.readStringUntil(',');
    waterPumpDuration = serialPi.readStringUntil('\n');
//    if (// distance > criticalDistance){ //if the water pump message is not correct then stop algorithm
//      packet += waterPumpStatus;
//      return;
//    }
    initialDistance = distance; //find the initial water level
    TIMSK1 |= (1 << OCIE1A);
  }
  packet += "\"waterPumpStatus\": " + String(waterPumpStatus) + ",";
}

void getWaterLevel(void){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.034/2;
  // Prints the distance on the Serial Monitor

  packet += "\"waterDistance\": " + String(distance);
  packet += ",";

  //If no voltage is supplied to the ultrasonic sensor then turn on the debugging LED 
  if(abs(distance - 0) < 0.01){
    digitalWrite(distanceLED, HIGH);
    waterDistanceStatus = false;
  }
  else{
    digitalWrite(distanceLED, LOW); 
    waterDistanceStatus = true;  
  }
  packet += "\"waterDistanceStatus\": " + String(waterDistanceStatus) + ",";
}


void getLDR(void){
  ldrValue = analogRead(ldrPin);

  

   packet += "\"light\": " + String(((ldrValue-ldrLower)/ldrRange * 100)) + ",";
   
   //If the light is detected to be below 64% turn on the LED
   if ((ldrValue-ldrLower)/ldrRange <= 0.64) {
    digitalWrite(ldrLED, HIGH);
    
    ldrStatus = true;
   } else {
    digitalWrite(ldrLED, LOW);
    ldrStatus = false;
   }
  packet += "\"ldrStatus\": " + String(ldrStatus) + ",";
   
}

void getSoilMoisture(void){
  sensorValue = analogRead(soilMoisturePin); 
  packet += "\"soilMoisture\": " + String(sensorValue) + ",";

  //If no voltage is supplied to the moisture sensor then turn on the debugging LED 
  if (analogRead(soilMoisturePin) == 0){ 
    //digitalWrite(soilMoistureLED, HIGH);
    soilMoistureStatus = false;
  } else{
    //digitalWrite(soilMoistureLED, LOW);
    soilMoistureStatus = true;
  }
  packet += "\"soilMoistureStatus\": " + String(soilMoistureStatus);
}


ISR(TIMER1_COMPA_vect){
  seconds++;
  if(seconds == waterPumpDuration.toInt()){
    digitalWrite(pumpPin, LOW);
    TIMSK1 &= ~(1 << OCIE1A);

    //check change in distance and uopdate waterPumpStatus if needed
  }
  
}
