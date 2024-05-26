"""
THis script moves the servos in a sine and cosine wave pattern. 
The angles are calculated using the sine and cosine functions. """


import math
import time
import serial

from detect_lib import send_angles

# Configuration
serial_port = '/dev/tty.usbmodem2244301'  # Change this to your serial port
baud_rate = 115200
period = 3  # Period in seconds for a full wave
update_interval = 0.05  # Update interval in seconds (20 ms)

def generate_angles(t):
    angle1 = (math.sin(2 * math.pi * t / period) + 1) * 90  # Sine wave from 0 to 180
    angle2 = (math.cos(2 * math.pi * t / period) + 1) * 90  # Cosine wave from 0 to 180
    return angle1, angle2

def main():
    try:
        ser = serial.Serial(serial_port, baud_rate)
        ser.timeout = 0
        print(f"Opened serial port {serial_port}")
    except serial.SerialException:
        ser = None
        print(f"Could not open serial port {serial_port}, outputting to stdout")
        return

    start_time = time.time()
    while True:
        t = time.time() - start_time
        angle1, angle2 = generate_angles(t)
        r = send_angles(ser, angle1, angle2)
        print(f"Sent angles: {angle1:.2f}, {angle2:.2f} | {r}")

# call main with main guard
if __name__ == "__main__":
    main()