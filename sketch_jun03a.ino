int dir = 0;
int pul = 0;
int dirpin = 0;
int pulpin = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  while (Serial.available() >0) {
    dir = Serial.readStringUntil(",");
    Serial.read();
    pul = Serial.readStringUntil(",");
    Serial.read();
    dirpin = Serial.readStringUntil(",");
    Serial.read();
    pulpin = Serial.readStringUntil("\n");
  }

  pinMode(dirpin, OUTPUT);
  pinMode(pulpin, OUTPUT);

  
  if (dir == 1) {
    digitalWrite(dirpin, HIGH);
  }
  if (dir == 0) {
    digitalWrite(dirpin, LOW);
  }
  
  for (int i = 0; i<=pul; i++) {
    digitalWrite(pulpin, HIGH);
    delayMicroseconds(100);
    digitalWrite(pulpin, LOW);
    delayMicroseconds(100);
  }

  Serial.println("Done\n");
}
 
void loop() {
  // put your main code here, to run repeatedly:
  
}
