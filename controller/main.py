# Imports go at the top
from microbit import *
from utime import ticks_ms, ticks_diff
import math

class Servo:

    """
    A simple class for controlling hobby servos.

    Args:
        pin (pin0 .. pin3): The pin where servo is connected.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between minimum and maximum positions.

    Usage:
        SG90 @ 3.3v servo connected to pin0
        = Servo(pin0).write_angle(90)
    """

    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.analog_period = 0
        self.pin = pin
        analog_period = round((1/self.freq) * 1000)  # hertz to miliseconds
        self.pin.set_analog_period(analog_period)

        self.pos = angle

    def write_us(self, us):
        us = min(self.max_us, max(self.min_us, us))
        duty = round(us * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)
       

    def movea(self, degrees):
        degrees = degrees % 360 
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)
        self.pos = degrees

    def mover(self, degrees):
        pos = max(0, min(self.pos+degrees, 180))

        self.movea(pos)


def uart_readline(uart, timeout_ms=None) -> bytes:
    """
    Read a full line from UART, blocking until newline or optional timeout.

    :param uart: UART object (e.g., uart0)
    :param timeout_ms: Timeout in milliseconds (optional)
    :return: Decoded line as a string (excluding newline), or None on timeout
    """
    import time

    buffer = bytearray()
    start = time.ticks_ms()

    while True:
        if uart.any():
            char = uart.read(1)
            if char:
                buffer += char
                if char == b'\n':
                    return buffer
        else:
            if timeout_ms is not None:
                if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
                    return b''
        # Let other tasks run
        time.sleep_ms(1)

def map_xy_to_grid(x, y):
    """
    Map x and y from range 0 - 180 to integer grid coordinates 0 - 4.

    :param x: int, in range 0-180
    :param y: int, in range 0-180
    :return: tuple (x_mapped, y_mapped), both in range 0-å4
    """
    def map_value(v):
        return min(4, round(v / 180 * 4))

    return map_value(x), map_value(y)


uart.init(baudrate=115200)

sx = Servo(pin0)
sy = Servo(pin1)

x = y = 90
m = '' 

while True:
    if uart.any:
        try:
            s = uart_readline(uart, 100)
            if s:
               
                m, x, y = s.decode().split()
                x = int(x)
                y = int(y)

                # Move servos to commanded positions
                if m == 'a':
                    sx.movea(x)
                    sy.movea(y)
                elif m == 'r':
                    
                    sx.mover(x)
                    sy.mover(y)
                    
                    uart.write("x="+str(sx.pos)+" y="+str(sy.pos)+"\n")
                    x = y = 0 # Relative move so we have to clear it. 
                    
                # Map to grid and update display
                px, py = map_xy_to_grid(x, y)
                display.clear()
                display.set_pixel(px, py, 9)
        
    
                
        except Exception as e:
            uart.write("error: " + str(e) + "\n")




