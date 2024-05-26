# face-follower

A simple demo of programming a pan-tilt servo rig to move a camera to put the
center of the image at the centroid of a color object. 

The purpose of this project was not entirely to create a face-follower, but
rather to create it by having AI do most of the programming. Both the Arduino
and Host Python programs were almost entirely generated with a conversation
with ChatGPT.

## Use

The `servo` program runs on an Arduino that is connected to an I2C 16 port
servo driver. ( A4 -> SDA, A5->SDL)

1. Load the `servo` program onto an Arduino
2. Edit `follow.py` to reference the serial device of the Arduino.

Once it is running, the pan-tilt should hunt around to find a red object. 

## Videos

( Click to watch )

A view from the camera, showing the object bounding box and centroid
[![Camera View](https://img.youtube.com/vi/ywGxtKd_LxQ/0.jpg)](https://www.youtube.com/watch?v=ywGxtKd_LxQ)

A view of the Pan-tilt device. 
[![Servo View](https://img.youtube.com/vi/xhm9eCSPkeo/0.jpg)](https://www.youtube.com/watch?v=xhm9eCSPkeo)
