/*
Reads 3 32-bit integers from Serial and sets the first two to the angles of the first two servos, using an 
Adafruit 16-channel PWM/Servo driver.  ( Actually any PCA9685 will do ). 

The angles are in servo degrees, 0 to 180, and are scaled by 10000.  The data packet
incluide several checks for integrity.
*/

#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver board1 = Adafruit_PWMServoDriver(0x40);  // default address 0x40

#define SERVOMIN  125  // minimum pulse length count (out of 4096)
#define SERVOMAX  625  // maximum pulse length count (out of 4096)

int angleToPulse(float ang) {
  int pulse = map((int)ang, 0, 180, SERVOMIN, SERVOMAX);  // map angle of 0 to 180 to Servo min and Servo max
  return pulse;
}

int decode_angle(int32_t angle) {

  int decoded = (angle - 1800000) / 10000;

  if (decoded == -180) {
    decoded = -179;  // Adjust to avoid ambiguity with zero encoding
  }
  return decoded;

}

// Define the updated data structure
struct ServoData {
  int32_t angle1;   // Angle for servo 1, must not be zero
  int32_t angle2;   // Angle for servo 2, must not be zero
  uint8_t code;  // A short code that must not be 0
  uint8_t terminator;  // Must be 0
};

/**
  Python code to send data using the struct module:
  
  import struct

  angle1 = 90 * 10_000  # Example: 90.0000 degrees scaled by 10000
  angle2 = 45 * 10_000  # Example: 45.0000 degrees scaled by 10000
  code = 123  # Example: a non-zero short value

  data = struct.pack('<iiBB', angle1, angle2, code, 0)
  serial.write(data)
*/

void setup() {
  Serial.begin(115200);
  board1.begin();
  board1.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  while (!Serial) {
    ; // Wait for Serial to be ready
  }
  Serial.println("ready.");
}

// Array to keep track of the last angles for the servos
float lastAngles[2] = {0.0, 0.0};

ServoData data;

void loop() {
  if (Serial.available() >= sizeof(ServoData)) {  // Check if enough bytes are available

    Serial.readBytes((char*)&data, sizeof(ServoData));  // Read data into the struct

    if ( (char)data.code == '?'){
      // Status request
      Serial.println("ready.");
      return;
    }

    // Validate the data
    if ( data.code == 0 || data.angle1 == 0 || data.angle2 == 0 || data.terminator != 0) {
      Serial.println("Error (framing or invalid data)");
      while (Serial.read() != 0) {
        // Do nothing, just consume bytes until the next zero
      }
      return;
    }

    if (data.code != 'a' && data.code != 'r') {
      Serial.println("Error (invalid code)");
      return;
    }

    // Convert angles to float and scale
    float angle1 = decode_angle(data.angle1);
    float angle2 = decode_angle(data.angle2);


    // Set angles to servos
    for (int i = 0; i < 2; i++) {
      
      float angle = (i == 0) ? angle1 : angle2;

      if ((char)data.code == 'r') {
        // Add to the angle the corresponding value in lastAngles
        angle += lastAngles[i];
        if (angle > 180) angle = 180;  // Clamp to max angle
        if (angle < 0) angle = 0;     // Clamp to min angle
      } else {
        if (angle > 180 || angle < 0) {
          Serial.print("Error (angle out of range): ");
          Serial.println(angle);
          return;
        }
      }

      int pulse = angleToPulse(angle);
      board1.setPWM(i, 0, pulse);

      lastAngles[i] = angle;

      // Print the servo number, angle, and pulse

      Serial.print  ("pos: ");
      Serial.print  (lastAngles[0]);
      Serial.print  (" ");
      Serial.println(lastAngles[1]);
      
    }
  } 
}
