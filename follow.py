import cv2
import numpy as np
import sys
from detect_lib import detect_color
from ptservo import PTServoMB

# Configuration
serial_port = '/dev/tty.usbmodem2212202'  # Change this to your serial port
baud_rate = 115200

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

def main():
    pt_servo = PTServoMB(serial_port, baud_rate)
    centroid_scaled = None

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

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
        else:
            centroid_scaled = None
       
        processed_frame = cv2.resize(processed_frame, (800, int(800 * frame.shape[0] / frame.shape[1]))) # rescale to 800x800
     
        
        cv2.imshow('Red Object Detection', processed_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            sys.exit()
        elif centroid_scaled is not None:

            pt_servo.update_angles(centroid_scaled)

        #print(pt_servo.get_status())

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
