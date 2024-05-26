#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver board1 = Adafruit_PWMServoDriver(0x40);  // default address 0x40

#define SERVOMIN  125  // minimum pulse length count (out of 4096)
#define SERVOMAX  625  // maximum pulse length count (out of 4096)

int angleToPulse(float ang) {
  int pulse = map((int)ang, 0, 180, SERVOMIN, SERVOMAX);  // map angle of 0 to 180 to Servo min and Servo max
  return pulse;
}

void setup() {
  Serial.begin(115200);
  Serial.println("16 channel Servo test!");
  board1.begin();
  board1.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
}

void loop() {
  if (Serial.available() >= 12) {  // 3 * 32-bit integers = 12 bytes
    int32_t angles[3];
    Serial.readBytes((char*)angles, 12);  // Read 12 bytes

    if (angles[2] != 0 || angles[0] == 0 || angles[1] == 0 ) {
      // Discard the data and keep reading until we find a zero
      Serial.println("Error (framing)");
      while (Serial.available() && Serial.read() != 0);

      return;
    }

    // Convert back to float and scale
    float angle1 = (float)angles[0] / 10000.0;
    float angle2 = (float)angles[1] / 10000.0;

    if (angle1 < 0 || angle1 > 180 || angle2 < 0 || angle2 > 180){
      // Discard the data and keep reading until we find a zero
      Serial.println("Error (values)");
      while (Serial.available() && Serial.read() != 0);
      return;
    }

    // Convert back to float and scale, then set angles to servos
    for (int i = 0; i < 2; i++) {
      float angle = (float)angles[i] / 10000.0;
      int pulse = angleToPulse(angle);
      board1.setPWM(i, 0, pulse);

      // Print the servo number, angle, and pulse
      
      /*Serial.print("Servo ");
      Serial.print(i + 1);
      Serial.print(" Angle: ");
      Serial.print(angle);
      Serial.print(" Pulse: ");
      Serial.println(pulse);*/
      
    }
  }
}
