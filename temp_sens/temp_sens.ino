#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

bool sendData = false;  // flag to control sending

void setup() {
  Serial.begin(9600);
  mlx.begin();
}

void loop() {
  // Check for Pi commands
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "TEMP") {
      sendData = true;
    }
    else if (cmd == "STOP") {
      sendData = false;
    }
  }

  // Send data continuously if flag is set
  if (sendData) {
    float ambient = mlx.readAmbientTempC();
    float object = mlx.readObjectTempC();
    Serial.print(ambient);
    Serial.print(",");
    Serial.println(object);
    delay(500); // send every 0.5s
  }
}
