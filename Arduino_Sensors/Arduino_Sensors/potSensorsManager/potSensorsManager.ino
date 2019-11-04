#define serialPi Serial
#include <ArduinoJson.h>



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

//Function prototypes
void getLDR(void);
void getWaterLevel(void);
void getSoilMoisture(void);
void waterPumpManager(void);
void setup() {

  pinMode(ldrLED, OUTPUT);
  pinMode(distanceLED, OUTPUT);
  pinMode(soilMoistureLED, OUTPUT);
  
  //Set the sensor pins
  pinMode(ldrPin, INPUT);
  pinMode(soilMoisturePin, INPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

 // initialize timer1 
  noInterrupts();           // disable all interrupts
  TCCR1A = 0;
  TCCR1B = 0;

  // Set timer1_counter to the correct value for our interrupt interval
  timer1_counter = 3124; 
  TCNT1 = timer1_counter;   // preload timer
  // Set CS11 bit for 8 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  interrupts();
  TIMSK1 &= ~(1 << TOIE1); //Disable timer1 interrupts
  
  serialPi.begin(9600); //begin serial on port 9600

}

void loop() {
  timerIterations = 0;
  packet = "";
  packet += 0x08; //The OpCode for the data packet
  packet += ",";
  packet += nPacket;
  packet += ",";
  
  getWaterLevel();
  getLDR();
  getSoilMoisture();
  serialPi.println(packet);
  //Timer1.attachInterrupt(timerIsr); // attach the service routine here
  TIMSK1 |= (1 << TOIE1);
  while((TIMSK1 & (1 << TOIE1))){ //Once the interrupt is disabled, continue with regular loop
    if(resendPacket){
      serialPi.println(packet);
      resendPacket = false;
    }
  } 
  
  delay((waitFor - (timerIterations * 5)) * 1000); //waitFor the remaining time left in the delay
  nPacket = (nPacket + 1) % 100;
  
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

  packet += distance;
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
  packet += waterDistanceStatus;
  packet += ",";
}


void getLDR(void){
  ldrValue = analogRead(ldrPin);

  

   packet += (ldrValue-ldrLower)/ldrRange * 100;
   packet += ",";
   
   //If the light is detected to be below 64% turn on the LED
   if ((ldrValue-ldrLower)/ldrRange <= 0.64) {
    digitalWrite(ldrLED, HIGH);
    ldrStatus = true;
   } else {
    digitalWrite(ldrLED, LOW);
    ldrStatus = false;
   }
  packet += ldrStatus;
  packet += ",";
   
}

void getSoilMoisture(void){
  sensorValue = analogRead(soilMoisturePin); 
  packet += sensorValue;
  packet += ",";

  //If no voltage is supplied to the moisture sensor then turn on the debugging LED 
  if (analogRead(soilMoisturePin) == 0){ 
    digitalWrite(soilMoistureLED, HIGH);
    soilMoistureStatus = false;
  } else{
    digitalWrite(soilMoistureLED, LOW);
    soilMoistureStatus = true;
  }
  packet += soilMoistureStatus;
}

ISR(TIMER1_OVF_vect){
  TCNT1 = timer1_counter;   // preload timer
  timerIterations++;
  //serialPi.println("made it to ISR\nIteration: " + timerIterations);
  
  while(serialPi.available() > 0 ){ // Don't read unless there is data 
    String ack = serialPi.readStringUntil(',');
    String n = serialPi.readStringUntil('\0');

    if(ack == "00" && n == String(nPacket)){// && packetRec.toInt() == nPacket){
      TIMSK1 &= ~(1 << TOIE1);
    }
    else{
      resendPacket = true;
    }
    }
    
    if(timerIterations >= waitFor / 5){
      TIMSK1 &= ~(1 << TOIE1); //disable timer
    }
 
    
    
  
}
