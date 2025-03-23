"""Send commands to the Micropython controller over serial."""
import serial
import time
import math

def figure_8_generator():
    """Yields x and y values tracing a figure-8 pattern."""
    t = 0
    while True:
        x = int(90 + 87 * math.sin(math.radians(t)))
        y = int(90 + 87 * math.sin(math.radians(2 * t)))
        yield x, y
        t = (t + 3) % 360

def flex():
    """Yields x and y values moving from (0, 0) to (180, 180)."""
    while True:
       
        for x,y in [(0,0), (0,180), (180,180), (180,0), (180, 180)]:
            print('-'*20)
            yield x,y
        return

def send_characters():
    # Open the serial port
    print("Opening")
    with serial.Serial('/dev/tty.usbmodem2212202', baudrate=115200, timeout=1) as ser:
        print("Opened")
        
        generator = figure_8_generator()
        for x, y in generator:
            message = f"{x} {y}\n"
            #print(f"S: {message}")
            ser.write(message.encode())
                
            # Check for incoming data
            while ser.in_waiting > 0:
                incoming_data = ser.read(ser.in_waiting).decode()
                print(incoming_data, end='')
            
            time.sleep(.05)
            
            #print("\033[H\033[J", end="")


if __name__ == "__main__":
    send_characters()
