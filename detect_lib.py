import cv2
import numpy as np
import signal
import sys


def detect_yellow_object(frame, mask):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create mask for the yellow range
    mask = cv2.inRange(hsv, mask['lower'], mask['upper'])
    
    # Apply morphological operations to remove noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Collect HSV values of the detected yellow object
        mask_contour = np.zeros_like(mask)
        cv2.drawContours(mask_contour, [largest_contour], -1, 255, thickness=cv2.FILLED)
        hsv_values = hsv[mask_contour == 255]

    
    return frame
