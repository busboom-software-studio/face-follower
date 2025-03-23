import cv2
import numpy as np
import sys
from detect_lib import detect_color
from ptservo import PTServoMB, PTServoArduino
from pynput import keyboard
from simple_pid import PID
from time import sleep

# Configuration
serial_port = '/dev/tty.usbmodem2212201' # Arduino
#serial_port = '/dev/tty.usbmodem2212202' # Micro:bit
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

manual_key_map = {
        ord('w'): (0, 5),   # Up
        ord('s'): (0, -5),  # Down
        ord('d'): (5, 0),   # Right
        ord('a'): (-5, 0)   # Left
    }

def kbd_move():
    """Yields x and y values from keyboard input using cv2.waitKey."""
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key != 255:
            print(key)
        if key == ord('q') or key == 27:  # ESC key to exit manual mode
            yield False, None, None
        elif key == ord('w'):  # Up
            yield True, 0, 5
        elif key == ord('s'):  # Down
            yield True, 0, -5
        elif key == ord('d'):  # Right
            yield True, 5, 0
        elif key == ord('a'):  # Left
            yield True, -5, 0
        else:
            sleep(0.1)

def main():
    #pt_servo = PTServoMB(serial_port, baud_rate)
    pt_servo = PTServoArduino(serial_port, baud_rate)
    
    pt_servo.move_a(90, 90)
    
    pid_y = PID(Kp=-3, Ki=0.01, Kd=0.5, setpoint=0)
    pid_x = PID(Kp=6, Ki=0.01, Kd=0.5, setpoint=0)
    
    
    centroid_scaled = None 
    manual_mode = True

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            sleep(2)
            break
        
        processed_frame, centroid = detect_color(frame, red_mask)
        
        if centroid is not None:
            centroid_x = int(centroid[0])
            centroid_y = int(centroid[1])
            centroid_scaled = (centroid[0] / frame.shape[1] * 2 - 1, centroid[1] / frame.shape[0] * 2 - 1)
            
            servo_target = (round(pid_x(centroid_scaled[0])), round(pid_y(centroid_scaled[1])))
            
            cv2.circle(processed_frame, (centroid_x, centroid_y), 5, (0, 255, 0), -1)
        else:
            centroid = None
            centroid_scaled = None
            servo_target = (0, 0)
       
        processed_frame = cv2.resize(processed_frame, (800, int(800 * frame.shape[0] / frame.shape[1]))) # rescale to 800x800
     
        
        cv2.imshow('Red Object Detection', processed_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == 27:
            sys.exit()
        elif key == ord('m'):
            manual_mode = not manual_mode
            
            if manual_mode:
               print("Manual mode enabled")
            else:
                print("Manual mode disabled")
                
            sleep(1)
            cv2.waitKey(1)  # Clear any pending key events
        
        elif manual_mode and key in manual_key_map:
             
            x, y = manual_key_map[key]
                
            pt_servo.move_r(x, y)
            
        elif centroid_scaled is not None:

            if not manual_mode:
                pt_servo.move_r(servo_target[0], servo_target[1])
        
        sleep(0.01) # wait to update status
        pt_servo.get_status()
        
        print("\033[H\033[J", end="")  # Clear the terminal using ANSI escape codes
        if manual_mode:
            print("Manual mode")
        else:
            print("Auto mode")
        
        print(f"Servo pos:     x={pt_servo.x}, y={pt_servo.y}")
        
        if centroid_scaled is not None:
            print(f"Centroid:      x={centroid[0]:4d}, y={centroid[1]:4d}")
            print(f"Cent. Scaled:  x={centroid_scaled[0]:1.3f}, y={centroid_scaled[1]:1.3f}")
            print(f"Servo target:  x={servo_target[0]:.4f}, y={servo_target[1]:.4f}")
        
        
        
        print("Last response:")
        print(pt_servo.last_response)
    
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
