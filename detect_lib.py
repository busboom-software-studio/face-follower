"""
This module provides functions for detecting objects of a specific color in a frame and sending angles to a serial port.
"""

import struct
import cv2
import numpy as np
import signal
import sys
from serial import Serial



def detect_color(frame, mask):
    """
    Detects the largest object of a specific color in a frame.
    
    Args:
        frame (np.array): The frame to process.
        mask (dict): A dictionary containing the lower and upper bounds of the color range.
    
    Returns:
        tuple: A tuple containing the processed frame and the centroid of the largest contour.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create mask for the orange range
    if len(mask) == 2:
        mask = cv2.inRange(hsv, mask['lower'], mask['upper'])
    else:
        mask1 = cv2.inRange(hsv, mask['lower1'], mask['upper1'])
        mask2 = cv2.inRange(hsv, mask['lower2'], mask['upper2'])
        mask = cv2.bitwise_or(mask1, mask2)

    
    # Apply morphological operations to remove noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    centroid = None
    if contours:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Calculate the centroid of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centroid = (cX, cY)
            cv2.circle(frame, centroid, 5, (0, 0, 255), -1)
    
    return frame, centroid


def send_angles(ser: Serial, angle1 : float, angle2: float ):
    """
    Sends angles to a serial port.
    
    Args:
        ser: The serial port object.
        angle1 (float): The first angle to send.
        angle2 (float): The second angle to send.
    
    Returns:
        str: The response received from the serial port.
    """
    # Convert angles to 32-bit integers
    angle1_int = max(int(angle1 * 10000), 1)
    angle2_int = max(int(angle2 * 10000), 1)
    data = struct.pack('iii', angle1_int, angle2_int, 0)

    if ser:
        ser.write(data)
        response = ser.readline().decode().strip()  # Read a line from the serial port
        return response
