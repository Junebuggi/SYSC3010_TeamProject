#define serialPi Serial
// #include <ArduinoJson.h>

const float criticalDistance = 20;

//Declare constant variables
const int potID = 1;
const double ldrLower = 390; //the value when the LDR is complete darkness
const double ldrUpper = 685; //the value when the LDR is in complete brightness
const double ldrRange = ldrUpper-ldrLower;

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
const int ackLED = 5;

// Define sensor variables
int ldrValue;
long duration;
float distance;
int sensorValue;  
float initialDistance;
int waterPumpDuration;
int seconds = 0;
boolean waterPumpMessageIntercept = false;

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
  pinMode(pumpLED, OUTPUT);
  pinMode(pumpPin, OUTPUT);
  pinMode(ackLED, OUTPUT);
  
  //Set the sensor pins
  pinMode(ldrPin, INPUT);
  pinMode(soilMoisturePin, INPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  digitalWrite(pumpPin, HIGH);

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
  
  boolean flag = false;
  if(serialPi.available() > 0){
    
    String opcode = serialPi.readStringUntil(',');
    
    if (opcode == "E") { // The roomPi is requesting potSensorData
      getSensorData();
      waterDistanceStatus = true;
      int startWaitingTime = millis();
      flag = true;
      while (serialPi.available() > 0 && millis() < startWaitingTime + 1000 && flag){
        String opcode = serialPi.readStringUntil(',');
        if (opcode == "0") {
          digitalWrite(pumpLED, !digitalRead(pumpLED));
          flag = false; // Exit nested loop
        }
        else {
          serialPi.println(packet);
        }
      }

      }
//      while(millis() < startWaitingTimer + 1000){ // Wait 
//          if(serialPi.available() > 0) {
//            String opcode = serialPi.readStringUntil(',');
//            
//            if (opcode == "0") {
//              digitalWrite(ackLED, !digitalRead(ackLED));
//              flag = true; // Exit nested loop
//              break;
//            }
//            else if (opcode == "C") {
//              waterPumpDuration = serialPi.readStringUntil('\n'); // Read the rest of the string
//              waterPumpMessageIntercept = true; //Set the flag so the pumpManager function knows a waterPump message has been intercepted
//            }
//          }
//          serialPi.flush();
//          if (flag == true){
//          
//            break;
//          
//          }
//      }
//    }

    else if (opcode = "C") { //|| waterPumpMessageIntercept) { // The roomPi is requesting for the water pump to be turned on
      
      //if (!waterPumpMessageIntercept) {
        waterPumpDuration = serialPi.readStringUntil('\n').toInt();
        if(waterPumpDuration >= 1) {
                  digitalWrite(pumpLED, HIGH);
       
      //}
      digitalWrite(pumpPin, LOW);
      initialDistance = distance; // Find the initial water level
      TIMSK1 |= (1 << OCIE1A); // Enable the timer
    
        }
 waterPumpMessageIntercept = false; // Reset the flag
    }
  }

 //while(serialPi.available() > 0) { serialPi.read(); } //Flush any leftover values
  
}

void getSensorData(void) {
  
  packet = "{\"opcode\": 8, \"potID\": " + String(potID);
  packet += ",";
  packet += "\"waterDistanceStatus\": " + String(waterDistanceStatus) + ",";
  getWaterLevel();
  getLDR();
  getSoilMoisture();
  packet += "}";
  serialPi.println(packet);
  
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
  if (seconds >= waterPumpDuration) {
    digitalWrite(pumpPin, HIGH);
    //delay(100);
    TIMSK1 &= ~(1 << OCIE1A);
    seconds = 0;
    //serialPi.println("Pump Finished");
    if ( (initialDistance - distance) <= 0.1) {
      waterDistanceStatus = false; // The water levels did not decrease when the pump was suppose to be on
    }
  } 
}
