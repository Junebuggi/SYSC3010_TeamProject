#define serialPi Serial

const int potID = 1;
int temp;
int ldrStatus;
int moisture;
const int moisturePin = A2;
const int tempPin = A1;
const int ledPin = 13;
const int ldrPin = A0;
const double ldrLower = 390;
const double ldrUpper = 685;
const double ldrRange = ldrUpper-ldrLower;
int thresholdValue = 800;

void setup() {

  //Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(ldrPin, INPUT);
  pinMode(tempPin, INPUT);
  pinMode(moisturePin, INPUT);
  serialPi.begin(9600);

}

void loop() {
    ldrStatus = analogRead(ldrPin);
    int ldrPer = (ldrStatus-ldrLower)/ldrRange * 100;
    moisture = analogRead(moisturePin);
    temp = analogRead(tempPin);
    float tempFloat = (temp/1024.0)*5000;
    float cel = tempFloat/10;
    double moistPer = abs(100.0 -(moisture-405.0)/619.008 * 100.0);
    serialPi.print(potID);
    serialPi.print(",");
    serialPi.print((ldrStatus-ldrLower)/ldrRange * 100);
    serialPi.print(",");
    serialPi.print(cel);
    serialPi.print(",");
    serialPi.println(moistPer);
 
    //serialPi.println("%");
    
  if ((ldrStatus-ldrLower)/ldrRange <= 0.64) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
  delay(2000);
}
