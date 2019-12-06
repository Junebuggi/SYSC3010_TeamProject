#include <Wire.h>
#include <LiquidCrystal_I2C.h>


LiquidCrystal_I2C lcd(0x20, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

void setup()
{
  Serial.begin(9600);
  
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(0,1);
  lcd.print("hello world!");
  
}

void loop() {

}
