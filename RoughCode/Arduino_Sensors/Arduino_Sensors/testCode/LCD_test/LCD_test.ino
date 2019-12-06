#include <Wire.h>
#include <LiquidCrystal_I2C.h>


LiquidCrystal_I2C lcd(0x20, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

void setup()
{
  Serial.begin(9600);
  
  lcd.begin(16, 2);
  lcd.clear();
  lcd.print("hello world!");
  
}

void loop(){
  int ldrStatus = analogRead(ldrPin);
  int ldrPer = (ldrStatus-ldrLower)/ldrRange * 100;
  char lightStat; 
  sprintf(lightStat, "Light: %f%", ldrPer); 
//  lcd.print(lightStat);
  if ((ldrStatus-ldrLower)/ldrRange <= 0.64) {
    digitalWrite(ledPin, HIGH);

    lcd.print("Light percentage: ");
    //lcd.println((ldrStatus-ldrLower)/ldrRange * 100);
    //delay(550);
  } else {
    digitalWrite(ledPin, LOW);
    //Serial.print("Light percentage: ");
    //Serial.print((ldrStatus - ldrLower)/ldrRange * 100);
    //Serial.println("%");


    
  }
  Serial.println(lightStat);
  //delay(150);
  
}
