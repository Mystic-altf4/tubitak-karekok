#define trigPin 4
#define echoPin 2
long sure, mesafe;

void setup () {
Serial.begin(9600);
pinMode(trigPin, OUTPUT);
pinMode(echoPin, INPUT);
}
void loop () {
digitalWrite(trigPin, LOW);
delayMicroseconds(3);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);

int sure = pulseIn(echoPin, HIGH);

int mesafe = (sure/2) * 0.0343;
Serial.print(mesafe);
delay(500);
}