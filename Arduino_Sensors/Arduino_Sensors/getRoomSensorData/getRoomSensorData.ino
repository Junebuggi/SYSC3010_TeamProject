#include "DHT.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define serialPi Serial
#define DHTPIN 2 //Digital pin connected to the DHT sensor
#define DHTTYPE DHT22 // DHT 22 (AM2302)

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

//Function prototypes
void getDHT(void);
void getLDR(void);

//Declare global and constant variables
const int potID = 1;
int ldrStatus;
const int ledPin = 13;
const int ldrPin = A0;
const double ldrLower = 390;
const double ldrUpper = 685;
const double ldrRange = ldrUpper-ldrLower;

LiquidCrystal_I2C lcd(0x20, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(ldrPin, INPUT);
  dht.begin();
  
  serialPi.begin(9600);

  lcd.begin(16, 2);
  lcd.clear();
}

void loop() {
    serialPi.print(potID);
    serialPi.print(",");
    getLDR();
    getDHT();

    serialPi.println("");
    

  delay(2000);
}

void getDHT(void){
  // Reading temperature or humidity takes about 250 milliseconds
  float h = dht.readHumidity();
  serialPi.print(h); //print the humidity to the serial port
  serialPi.print(",");
  
  // Reads temperature as Celsius
  float t = dht.readTemperature();
  serialPi.print(t); //print the temperature to the serial port
  serialPi.print(",");
  
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);
  serialPi.print(hic); //print the heat index to the serial port

  // The lcd displays the temperature and humidity values
  lcd.setCursor(0,0);
  lcd.clear();
  lcd.print("Temp: ");
  lcd.print(t);
  lcd.print((char)223);
  lcd.print("C");
  lcd.setCursor(0,1);
  lcd.print("Humidity: ");
  lcd.print(h);
  lcd.print("%");

  return;
}

void getLDR(void){
  ldrStatus = analogRead(ldrPin);

   serialPi.print((ldrStatus-ldrLower)/ldrRange * 100);
   serialPi.print(",");
   
   //If the light is detected to be below 64% turn on the LED
   if ((ldrStatus-ldrLower)/ldrRange <= 0.64) {
    digitalWrite(ledPin, HIGH);
   } else {
    digitalWrite(ledPin, LOW);
   }
}
