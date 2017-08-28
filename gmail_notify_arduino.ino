/* Receives a message from the python program when a new message is received and will send a message to arduino to move flag*/

#include <Servo.h>
String state;
Servo myservo;
int pos = 0; 
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  myservo.attach(9);
}


void sweep() {
  for (pos = 0; pos <= 90; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 90; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}

void loop() {

  if (Serial.available()) {     
    state = Serial.readString();   
    
    if (state == "1" ){
      Serial.write("New Message");
      digitalWrite(LED_BUILTIN, HIGH);
      sweep();
    }
    else {
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}
