#include <NewPing.h>

// Ultrasonic pins
#define TRIG 2
#define ECHO 3
NewPing sonar(TRIG, ECHO, 200); // Max distance = 200 cm

// Motor pins
#define IN1 8
#define IN2 9
#define IN3 10
#define IN4 11

char command;

void setup() {
  Serial.begin(9600);

  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
}

void loop() {
  delay(100);
  int distance = sonar.ping_cm();
  if (distance == 0) distance = 200; // fallback if no echo

  // Send current distance to Raspberry Pi
  Serial.print("DIST: "); Serial.print(distance); Serial.println(" cm");

  // Obstacle condition — override everything
  if (distance < 20) {
    stopMotors();
    Serial.println("OBSTACLE: <20cm - Stopping and Turning Left");
    delay(300);
    left();  // Turning left until clear
    return;
  }

  // If no obstacle, check for serial command
  if (Serial.available()) {
    command = Serial.read();

    // Ignore unwanted characters like newline or carriage return
    if (command == '\n' || command == '\r') return;

    move(command);
  }
}

void move(char cmd) {
  switch(cmd) {
    case 'f': forward();   Serial.println("CMD: f - Moving Forward"); break;
    case 'b': backward();  Serial.println("CMD: b - Moving Backward"); break;
    case 'l': left();      Serial.println("CMD: l - Turning Left"); break;
    case 'r': right();     Serial.println("CMD: r - Turning Right"); break;
    case 's': stopMotors();Serial.println("CMD: s - Stopping Motors"); break;
    default: Serial.print("CMD: "); Serial.print(cmd); Serial.println(" - Unknown Command"); break;
  }
}

void forward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}
void backward() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
}
void left() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}
void right() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
}
void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}
