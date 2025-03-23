#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
import signal
import sys
from detect_lib import *

# Define the initial range for yellow in HSV
blue_mask = {
    'lower': np.array([100, 150, 0]),
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
    # Capture video from the webcam
    cap = cv2.VideoCapture(0)


    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        processed_frame, centroid = detect_color(frame, red_mask)
        cv2.imshow('Object Detection', processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit()

    cap.release()
    cv2.destroyAllWindows()

main()
