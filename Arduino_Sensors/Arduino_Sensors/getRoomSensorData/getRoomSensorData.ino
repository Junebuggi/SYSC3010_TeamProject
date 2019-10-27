#define serialPi Serial

// Initialize DHT sensor


//Function prototypes

void getLDR(void);
void getWaterLevel(void);
void getSoilMoisture(void);

//Declare global and constant variables
const int potID = 1;
int ldrStatus;
const int ldrLED = 13;
const int distanceLED = 11;
const int ldrPin = A0;
const double ldrLower = 390;
const double ldrUpper = 685;
const double ldrRange = ldrUpper-ldrLower;
const int trigPin = 10;
const int echoPin = 9;
const int soilMoisturePin = A2;
const int soilMoistureLED = 8; 
int sensorValue;  
const int limit = 300;
// defines variables
long duration;
float distance;

void setup() {
  pinMode(ldrLED, OUTPUT);
  pinMode(distanceLED, OUTPUT);
  pinMode(soilMoistureLED, OUTPUT);
  pinMode(ldrPin, INPUT);
  pinMode(soilMoisturePin, INPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  
  
  serialPi.begin(9600);

}

void loop() {
  
  getWaterLevel();
  getLDR();
  getSoilMoisture();
  serialPi.println();
  

  delay(2000);
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

  serialPi.print(distance);
  serialPi.print(",");

  if(abs(distance - 0) < 0.01){
    digitalWrite(distanceLED, HIGH);
  }
  else{
    digitalWrite(distanceLED, LOW);   
  }
}


void getLDR(void){
  ldrStatus = analogRead(ldrPin);

   serialPi.print((ldrStatus-ldrLower)/ldrRange * 100);
   serialPi.print(",");
   
   //If the light is detected to be below 64% turn on the LED
   if ((ldrStatus-ldrLower)/ldrRange <= 0.64) {
    digitalWrite(ldrLED, HIGH);
   } else {
    digitalWrite(ldrLED, LOW);
   }
}

void getSoilMoisture(void){
  sensorValue = analogRead(soilMoisturePin); 
  serialPi.print(sensorValue);
  serialPi.print(",");

  if (analogRead(soilMoisturePin) == 0){
    digitalWrite(soilMoistureLED, HIGH);
  } else{
    digitalWrite(soilMoistureLED, LOW);
  }
}
