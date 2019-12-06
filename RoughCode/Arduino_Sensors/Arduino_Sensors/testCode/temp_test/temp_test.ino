float temp;
const int ldrPin = A0;

void setup() {
  Serial.begin(9600);
};

void loop () {
  temp = analogRead(ldrPin) * 5 / 1024.0;
  temp = temp - 0.5;
  temp = temp / 0.01;
  Serial.println(temp);
  delay(500);
};
