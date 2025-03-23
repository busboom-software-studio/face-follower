import cv2
import numpy as np
import math
import time
import serial
import sys
from detect_lib import send_angles_arduino, detect_color
from simple_pid import PID

# Configuration
serial_port = '/dev/tty.usbmodem22431401'  # Change this to your serial port
baud_rate = 115200

pid_param = {'Kp':4, 'Ki':0.05, 'Kd':0.05, 'setpoint':0}

pid_0 = PID(**pid_param)
pid_1 = PID(**pid_param)

try:
    ser = serial.Serial(serial_port, baud_rate)
    ser.timeout = 0
    print(f"Opened serial port {serial_port}")
except serial.SerialException:
    ser = None
    print(f"Could not open serial port {serial_port}, outputting to stdout")
    sys.exit()

blue_mask = {
        'lower': np.array([100, 150, 100]),
        'upper': np.array([140, 255, 255])
    }


# Red mask, using two ranges to capture the full spectrum of red
red_mask = {
    'lower1': np.array([0, 150, 150]),
    'upper1': np.array([10, 255, 255]),
    'lower2': np.array([170, 150, 150]),
    'upper2': np.array([180, 255, 255])
}



def pid_control(scaled_centroid, servo_0_angle, servo_1_angle):
    """Implement a PID controller to move the servos to the centroid of the object.  """
    angle_0 = pid_0(scaled_centroid[1])
    angle_1 = pid_1(scaled_centroid[0])
    return angle_0, angle_1


def main():
    servo_0_angle, servo_1_angle = 90, 90
    centroid_scaled = None

    # Capture video from the webcam
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        processed_frame, centroid = detect_color(frame, red_mask)
        
        if centroid is not None:
            centroid_x = int(centroid[0])
            centroid_y = int(centroid[1])
            centroid_scaled = (centroid[0] / frame.shape[1] * 2 - 1, centroid[1] / frame.shape[0] * 2 - 1)
            cv2.circle(processed_frame, (centroid_x, centroid_y), 5, (0, 255, 0), -1)

        processed_frame = cv2.resize(processed_frame, (800, int(800 * frame.shape[0] / frame.shape[1])))
        cv2.imshow('Yellow Object Detection', processed_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            sys.exit()
        elif key == 0:  # Up arrow key
            servo_0_angle = min(servo_0_angle + 4, 180)
        elif key == 1:  # Down arrow key
            servo_0_angle = max(servo_0_angle - 4, 0)
        elif key == 2:  # Left arrow key
            servo_1_angle = max(servo_1_angle + 4, 0)
        elif key == 3:  # Right arrow key
            servo_1_angle = min(servo_1_angle - 4, 180)
        elif centroid_scaled is not None:
            delta_0, delta_1 = pid_control(centroid_scaled, servo_0_angle, servo_1_angle)
            print(f"delta_0={delta_0}, delta_1={delta_1}")
            servo_0_angle -= delta_0
            servo_1_angle += delta_1

            if servo_0_angle < 0:
                servo_0_angle = 0
            elif servo_0_angle > 180:
                servo_0_angle = 180

            if servo_1_angle < 0:
                servo_1_angle = 0
            elif servo_1_angle > 180:
                servo_1_angle = 180

        r = send_angles_arduino(ser, servo_0_angle, servo_1_angle)

        print(r)

        print(f"servo_0_angle={servo_0_angle}, servo_1_angle={servo_1_angle}", end=' ')

        if centroid is not None:
            print(f"centroid={centroid_scaled}", end='')

        print()


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
