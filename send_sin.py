import math
import time
import serial
import struct

# Configuration
serial_port = '/dev/tty.usbmodem2244301'  # Change this to your serial port
baud_rate = 115200
period = 5  # Period in seconds for a full wave
update_interval = 0.01  # Update interval in seconds (20 ms)

def generate_angles(t):
    angle1 = (math.sin(2 * math.pi * t / period) + 1) * 90  # Sine wave from 0 to 180
    angle2 = (math.cos(2 * math.pi * t / period) + 1) * 90  # Cosine wave from 0 to 180
    return angle1, angle2

def main():
    try:
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Opened serial port {serial_port}")
    except serial.SerialException:
        ser = None
        print(f"Could not open serial port {serial_port}, outputting to stdout")
        return

    start_time = time.time()
    while True:
        t = time.time() - start_time
        angle1, angle2 = generate_angles(t)

        # Convert angles to 32-bit integers
        angle1_int = max(int(angle1 * 10000), 1)
        angle2_int = max(int(angle2 * 10000), 1)
        data = struct.pack('iii', angle1_int, angle2_int, 0)

        if ser:
            ser.write(data)
            # Read data back from UART and print it as strings
            if ser.in_waiting > 0:
                incoming_data = ser.read(ser.in_waiting).decode('utf-8')
                print(f"{incoming_data.strip()}")
                print('-------')
        else:
            print(f"{angle1_int} {angle2_int} 0")

        time.sleep(update_interval)  # Reduce the sleep time for smoother updates

if __name__ == "__main__":
    main()
