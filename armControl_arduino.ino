#include <Servo.h>
const byte numChars = 32;
char inChars[numChars];
char tempChars[numChars];
int theta1 = 0;
int theta2 = 0;
int theta3 = 0;
int theta4 = 0;

boolean receiving = false;

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

void setup() {
  // put your setup code here, to run once:
  int theta = 0;
  servo1.attach(2);
  servo2.attach(3);
  servo3.attach(4);
  servo4.attach(5);
  Serial.begin(9600);
}

void loop() {
  receive();
  if (receiving == true){
    strcpy(tempChars,inChars);
    parseData();
    
    //Serial.println(theta1);
    //Serial.println(theta2);
    //Serial.println(theta3);
    //Serial.println(theta4);
    
    servo1.write(theta1+90);
    servo2.write(theta2+90);
    servo3.write(theta3+90);
    receiving = false;
  }
}

void receive(){
  static bool inProgress = false;
  static byte ndx = 0;
  char start = '<';
  char end = '>';
  char rc;
  
  while (Serial.available() > 0 && receiving == false){
    rc = Serial.read();
    if (inProgress == true){
      if (rc != end){
        inChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars){
          ndx = numChars-1;
        }
      }
      else {
        inChars[ndx] = '\0';
        inProgress = false;
        ndx = 0;
        receiving = true;
      }
    }
    else if (rc == start){
      inProgress = true;
    }
  } 
}

void parseData(){
  char * strtokIndx;
  
  strtokIndx = strtok(tempChars,",");
  theta1 = atoi(strtokIndx);

  strtokIndx = strtok(NULL,",");
  theta2 = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ",");
  theta3 = atoi(strtokIndx);
}
