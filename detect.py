#!/usr/bin/env python
# coding: utf-8


import cv2
import numpy as np
from matplotlib import pyplot as plt

import cv2 

cap = cv2.VideoCapture(0)


def detect_red_objects(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red_1 = np.array([0, 120, 70])
    upper_red_1 = np.array([10, 255, 255])
    lower_red_2 = np.array([170, 120, 70])
    upper_red_2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    
    mask = cv2.bitwise_or(mask1, mask2)
    
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return frame


def draw_bounding_boxes(frame, mask):
    """
    Find contours in the mask and draw bounding boxes around the detected red objects in the frame.
        Parameters:
    - frame: The current frame from the web camera.
    - mask: The mask of the detected red color from the frame.
    Returns:
    - The frame with bounding boxes drawn around detected red objects.
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame



def detect_red_object(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define a very narrow range for the reddest red in HSV
    lower_red = np.array([0, 240, 240])
    upper_red = np.array([2, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # Apply morphological operations to remove noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the contour with the maximum intensity in the red channel
        reddest_contour = None
        max_intensity = 0
        for contour in contours:
            mask_contour = np.zeros_like(mask)
            cv2.drawContours(mask_contour, [contour], -1, 255, thickness=cv2.FILLED)
            mean_intensity = cv2.mean(hsv, mask=mask_contour)[0]
            if mean_intensity > max_intensity:
                max_intensity = mean_intensity
                reddest_contour = contour

        if reddest_contour is not None:
            x, y, w, h = cv2.boundingRect(reddest_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return frame



cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    processed_frame = detect_red_objects(frame)
    cv2.imshow('Red Object Detection', processed_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()




