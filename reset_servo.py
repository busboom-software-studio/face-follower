import math
import time
import serial
import sys

from detect_lib import send_angles

# Configuration
serial_port = '/dev/tty.usbmodem2244301'  # Change this to your serial port
baud_rate = 115200

try:
    ser = serial.Serial(serial_port, baud_rate)
    ser.timeout = 0
    print(f"Opened serial port {serial_port}")
except serial.SerialException:
    ser = None
    print(f"Could not open serial port {serial_port}, outputting to stdout")
    sys.exit()

for i in range(10):
    print(send_angles(ser, 0, 0))
    time.sleep(.1)

