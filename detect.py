#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
import signal
import sys
from detect_lib import detect_yellow_object

# Define the initial range for yellow in HSV
initial_mask = {
    'lower': np.array([20, 100, 100]),
    'upper': np.array([30, 255, 255])
}

def main():
    # Capture video from the webcam
    cap = cv2.VideoCapture(0)


    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        processed_frame = detect_yellow_object(frame, initial_mask)
        cv2.imshow('Yellow Object Detection', processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit()

    cap.release()
    cv2.destroyAllWindows()

main()
