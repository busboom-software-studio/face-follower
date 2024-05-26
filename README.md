# face-follower

A simple demo of programming a pan-tilt servo rig to move a camera to put the
center of the image at the centroid of a color object. 

## Use

The `servo` program runs on an Arduino that is connected to an I2C 16 port
servo driver. ( A4 -> SDA, A5->SDL)

1. Load the `servo` program onto an Arduino
2. Edit `follow.py` to reference the serial device of the Arduino.

Once it is running, the pan-tilt should hunt around to find a red object. 


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ywGxtKd_LxQ/0.jpg)](https://www.youtube.com/watch?v=ywGxtKd_LxQ)
