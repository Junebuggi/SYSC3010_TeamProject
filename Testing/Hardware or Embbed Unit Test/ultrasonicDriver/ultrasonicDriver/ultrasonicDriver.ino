
#include <math.h>

const int promptLED = 5; // Will blink to let you know you have 5 seconds until the next test
const int passLED = 8; //A green LED that blinks if the test passes
const int failLED = 11; //A red LED that blinks if the test fails

const int trigPin = 10;
const int echoPin = 9;

const int nTrials = 5;
const int promptTime = 5; //The number of seconds the promptLED blinks before the next trial starts

int nPass = 0;
int nFail = 0;

float readUltraSonic(void);
void runTest(int n, int trialDistance);
float runTrial(int n);
float getAverage(float arr[], int n);
float getMinimum(float arr[], int n);
float getMaximum(float arr[], int n);
float getVar(float arr[], int n, float mean);
float getStdDev(float mean);
void blinkN(int n, int LED);

void setup() {
  //Set the modes for the LEDs
  pinMode(promptLED, OUTPUT);
  pinMode(passLED, OUTPUT);
  pinMode(failLED, OUTPUT);

  //Set the modes for the ultrasonic pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Serial.begin(9600); //begin serial on port 9600
  
  //The ultra sonic sensor has a range of 2 to 400cm
  int distancesToTest[] = {400, 350, 300, 250, 200, 150, 100, 50, 2};

  for(int i = 0; i < 9; i++){
    runTest(nTrials, distancesToTest[i]);
  }

  Serial.println("================ Test Report ================");
  Serial.println("Total number of tests: " + String(nPass + nFail));
  Serial.println("Number of Successes: " + String(nPass));
  Serial.println("Number of Fails: " + String(nFail));
  Serial.println("Success Rate: " + String((double) nPass / nFail * 100) + "%"); 
  
}

void loop(){}

/**
   Polls the ultraSonic sensor

   @return the waterDistance in cm, represented as a float
*/
float readUltraSonic(void) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  return (duration * 0.034 / 2); //The distance to the water
}

void runTest(int n, int trialDistance){
  static int testNumber = 0;
  ++testNumber;
   Serial.println("================ Test " + String(testNumber) + ": " + String(trialDistance) + "cm ================");
   blinkN(promptLED, promptTime);
   float avg = runTrial(n);
   //The test passes
   if(abs((float) trialDistance - avg) <= 0.5){
    blinkN(1, passLED);
    nPass++;
    Serial.println("Test Passed\n");
   }
   else{
      blinkN(1, failLED);
      nFail++;
      Serial.println("Test Failed\n");
   }
   
}

float runTrial(int n){
  float distanceArray[n];
  
  for(int i = 0; i < n; i++){
    float distance = readUltraSonic();
    Serial.println("Trial " + String(i+1) + ": " + String(distance) + "cm"); 
    distanceArray[i] = distance; 
  }
  
  float avg = getAverage(distanceArray, n);
  Serial.println("Average: " + String(avg) + "cm");
  Serial.println("Maximum: " + String(getMaximum(distanceArray, n)) + "cm");
  Serial.println("Minimum: " + String(getMinimum(distanceArray, n)) + "cm");
  float var = getVar(distanceArray, n, avg);
  Serial.println("Variance: " + String(var));
  Serial.println("Standard Deviation: " + String(getStdDev(var)));
  
  return avg;
  
}

float getAverage(float arr[], int n) {
  float sum = 0.0;               
   for (int i = 0; i < n; ++i) {
      sum += arr[i];
   }
   return sum / n; //the average
}

float getMinimum(float arr[], int n){
  float min = arr[0];
  for(int i = 0; i < n; ++i){
    if(arr[i] < min){
      min = arr[i];
    }
  }
  return min;
}

float getMaximum(float arr[], int n){
  float max = arr[0];
  for(int i = 0; i < n; ++i){
    if(arr[i] > max){
      max = arr[i];
    }
  } 
  return max;
}

float getVar(float arr[], int n, float mean){
  float sumSquares = 0.0;
  for(int i = 0; i < n; ++i){
    sumSquares += pow(arr[i] - mean, 2); 
  }
  return sumSquares / n;
}

float getStdDev(float var){
  return sqrt(var);
}

void blinkN(int n, int LED){
  for(int i = 0; i < n*2; i++){
    digitalWrite(LED, !digitalRead(LED));
    delay(500);
  }
}
