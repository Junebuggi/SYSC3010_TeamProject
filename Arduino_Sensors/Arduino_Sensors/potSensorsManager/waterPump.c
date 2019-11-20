/*
    Pot sensors manager suggestions/modifications on waterpump manager
*/



//Relay pin configuration(from arduino)
const int pumpPin = 7;       //Pin connecting Arduino to relay
const int echoPin = 9;       //Pin connecting ultrasonic sensor to relay
const int trigPin = 10;      //Pin connecting ultrasonic sensor to relay     

//Water pump/Ultrasonic sensor variable declarations
float distance;             //Current water level in supply basin
float minimumDistance;      //Minimum level of water in supply basin required to water the plant
bool waterPumpStatus;       //Pump water success check
bool waterDistanceStatus;   //Water level success check
long duration;              //Time measurement taken by ultrasonic sensor

void setup(){
    pinMode(trigPin, OUTPUT);       //Setting the trigPin as an Output
    pinMode(pumpPin, OUTPUT);       //Setting the pin to output
    digitalWrite(pumpPin, LOW);     //Setting the pump off
    digitalWrite(trigPin, LOW);     //Setting the ultrasonic sensor reading off
}

/*Timer configuration*/


void loop(){

    if(serialPi.available() > 0 && serialPi.peek() == 'C' ){        //If start water pump message has been sent via opcode
        waterPumpManager();         //Call to water pump manager function
    }
}

void getWaterLevel(void){

    digitalWrite(trigPin, HIGH);        //Activate ultrasonic sensor
    delayMicroseconds(10);              //Keeps ultrasonic sensor on for 10 microseconds
    digitalWrite(trigPin, LOW);         //Turn off ultrasonic sensor
        
    duration = pulseIn(echoPin, HIGH);      //Reads the ultrasonic sensor, returns the sound wave travel time in microseconds
        
    distance = duration*0.034/2;     //Calculating the distance (converting from microseconds to cm)
 
    if(abs(distance - 0) < 0.01){       //If no voltage is supplied to the ultrasonic sensor (difference between readings are less than 0.01)
        waterDistanceStatus = false;        //If ultrasonic sensor reading was successfully taken
    }

    else{
        waterDistanceStatus = true;       //If ultrasonic sensor reading was successfully taken
    }
}

void waterPumpManager(void){

          
    if(distance - minimumDistance <= 0.5){//If difference between last measured water level and minimum acceptable distance to turn on pump is less than or equal to 0.5cm
        digitalWrite(pumpPin, LOW);           //Turn off pump 
        waterPumpStatus = false;              //If plant was successfully  watered
        //Turn on watering LED ?
    }
    
    if(distance - minimumDistance >= 1.0){//If difference between last measured water level and minimum acceptable distance to turn on pump is greater than or equal to 1cm
        digitalWrite(pumpPin, HIGH);        //Turn on pump using user defined value
        waterPumpStatus = true;              //If plant was successfully  watered
    }          
}