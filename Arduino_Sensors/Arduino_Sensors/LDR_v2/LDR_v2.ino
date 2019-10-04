#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int ledPin = 13;
const int ldrPin = A0;
const double ldrLower = 390;
const double ldrUpper = 685;
const double ldrRange = ldrUpper-ldrLower;

LiquidCrystal_I2C lcd(0x20, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

void setup() {

  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(ldrPin, INPUT);

  lcd.begin(16, 2);
  lcd.clear();
  //lcd.print("hello world!");

}

void loop() {
int ldrStatus = analogRead(ldrPin);
int ldrPer = (ldrStatus-ldrLower)/ldrRange * 100;
char lightStat; 
    Serial.print("Light percentage: ");
    Serial.print((ldrStatus-ldrLower)/ldrRange * 100);
    Serial.println("%");
    lcd.setCursor(0,0); // Sets the cursor to col 0 and row 0
    lcd.clear();
    lcd.print("Light Level: ");
    lcd.print(ldrPer);
    lcd.print("%");
    
//sprintf(lightStat, "Light: %f%", ldrPer); 
//  Serial.println(lightStat);
  if ((ldrStatus-ldrLower)/ldrRange <= 0.64) {
    digitalWrite(ledPin, HIGH);
//    Serial.print("Light percentage: ");
//    Serial.println((ldrStatus-ldrLower)/ldrRange * 100);
//    Serial.println("%");
    //delay(550);
  } else {
    digitalWrite(ledPin, LOW);
//    Serial.print("Light percentage: ");
//    Serial.print((ldrStatus - ldrLower)/ldrRange * 100);
//    Serial.println("%");
  }
  delay(1000);
}
