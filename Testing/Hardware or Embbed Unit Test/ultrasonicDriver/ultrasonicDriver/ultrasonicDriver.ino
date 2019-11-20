
/**
  SYSC 3010 Team Project: The Plant Nursery
  Team W4
  Name: ultrasonicDriver
  Purpose: A driver to test the hardware of the
           ultrasonic sensor

  @author Emma Boulay
  @version 1.3 14/11/19
*/

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

/*
 * The modes for the pins are set. Each test distance is run for n trials. 
 * After all the tests are run a Test Report Summary is outputed.
 */
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
  int distancesToTest[] = {150, 130, 110, 90, 70, 50, 30, 10, 2};

  for(int i = 0; i < 9; i++){
    runTest(nTrials, distancesToTest[i]);
  }

  Serial.println("================ Test Report Summary ================");
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

/*
 * Runs the test for n trials. If the average distance is within an 
 * acceptable margin of error to the test distance than the test passes
 * and a green LED will blink. Otherwise the test failed and a red LED 
 * will blink.
 */
void runTest(int n, int trialDistance){
  static int testNumber = 0;
  ++testNumber;
   Serial.println("================ Test " + String(testNumber) + ": " + String(trialDistance) + "cm ================");
   //Warn the user that the next test is about to begin
   blinkN(promptLED, promptTime);
   float avg = runTrial(n);
   //The test passes
   if(abs((float) trialDistance - avg) <= 0.5*4){
    blinkN(1, passLED);
    nPass++;
    Serial.println("Test Passed\n");
   }
   //The test fails
   else{
      blinkN(1, failLED);
      nFail++;
      Serial.println("Test Failed\n");
   }
   
}

/*
 * Runs all the trials for the test and outputs statistics output the 
 * data and its spread. Statistics include: Average, Maximum, Minimum,
 * Variance and Standard Deviation. These are indicators if the accuracy 
 * of the ultrasonic sensor
 * 
 * @param n the number of trials
 * @return the average distance in cm, represented as a float
 */
float runTrial(int n){
  float distanceArray[n];
  
  for(int i = 0; i < n; i++){
    delayMicroseconds(10);
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

/*
 * Computes the average of an array
 * 
 * @param arr the float array 
 * @param n the size of the array
 * @return the average of an array
 */
float getAverage(float arr[], int n) {
  float sum = 0.0;               
   for (int i = 0; i < n; ++i) {
      sum += arr[i];
   }
   return sum / n; //the average
}
/*
 * Computes the minimum of an array
 * 
 * @param arr the float array 
 * @param n the size of the array
 * @return the minimum value of an array
 */
float getMinimum(float arr[], int n){
  float min = arr[0];
  for(int i = 0; i < n; ++i){
    if(arr[i] < min){
      min = arr[i];
    }
  }
  return min;
}

/*
 * Computes the maximum of an array
 * 
 * @param arr the float array 
 * @param n the size of the array
 * @return the maximum value of an array
 */
float getMaximum(float arr[], int n){
  float max = arr[0];
  for(int i = 0; i < n; ++i){
    if(arr[i] > max){
      max = arr[i];
    }
  } 
  return max;
}

/*
 * Computes the variance of an array
 * 
 * @param arr the float array 
 * @param n the size of the array
 * @param mean the average of the array
 * @return the variance of the array
 */
float getVar(float arr[], int n, float mean){
  float sumSquares = 0.0;
  for(int i = 0; i < n; ++i){
    sumSquares += pow(arr[i] - mean, 2); 
  }
  return sumSquares / n;
}

 /*
 * Computes the standard deviation of an array
 * 
 * @param var the variance of the array
 * @return the standard deviation of an array
 */
float getStdDev(float var){
  return sqrt(var);
}

/*
 * An LED is blinked n times at the speed of 0.5 seconds per state (ON or OFF)
 * 
 * @param n the number of times to blink the LED
 * @param LED the LED to be blinked
 */
void blinkN(int n, int LED){
  for(int i = 0; i < n*2; i++){
    digitalWrite(LED, !digitalRead(LED));
    delay(500);
  }
}
