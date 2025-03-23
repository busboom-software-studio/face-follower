# Imports go at the top
from microbit import *
from utime import ticks_ms, ticks_diff
import math

class Servo:

    """
    A simple class for controlling hobby servos.

    Args:ß
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

    def write_us(self, us):
        us = min(self.max_us, max(self.min_us, us))
        duty = round(us * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)
       

    def write_angle(self, degrees=None):
        degrees = degrees % 360 if degrees else 0
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)

class PID:
    """
    A simple PID controller for servo position control.

    Args:
        kp (float): Proportional gain.
        ki (float): Integral gain.
        kd (float): Derivative gain.
        initial_position (int): Initial estimated position (default: 90).
    """
    def __init__(self, kp, ki, kd, initial_position=90):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.target_position = initial_position
        self.estimated_position = initial_position
        self.commanded_position = initial_position
        self.integral = 0
        self.previous_error = 0
        self.last_update_time = ticks_ms()
        self.time_delta = 0
        self.velocity = 0
        self.acceleration = 0


 


    def update(self, target_position, max_a=1_000_000):
        """
        Update the PID controller with a new target position.

        Args:
            target_position (int): The desired target position (0 to 180).

        Returns:
            int: The new commanded position.
        """
        current_time = ticks_ms()
        self.time_delta = ticks_diff(current_time, self.last_update_time) / 1000  # Convert to seconds
        self.last_update_time = current_time

        self.target_position = target_position
        error = self.target_position - self.estimated_position
        self.integral += error * self.time_delta
        derivative = (error - self.previous_error) / self.time_delta if self.time_delta > 0 else 0

        # PID formula
        adjustment = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        self.commanded_position = max(0, min(180, self.estimated_position + adjustment))

        # Compute velocity and acceleration
        new_velocity = (self.commanded_position - self.estimated_position) / self.time_delta if self.time_delta > 0 else 0
        self.acceleration = (new_velocity - self.velocity) / self.time_delta if self.time_delta > 0 else 0
        self.velocity = new_velocity


        # If acceleration exceeds the maximum allowed, adjust the commanded position
        if self.acceleration > max_a:
            max_change = max_a * (self.time_delta ** 2)  * -( self.acceleration / abs(self.acceleration))
            
            self.commanded_position = self.estimated_position - max_change
            self.commanded_position = max(0, min(180, self.commanded_position))
         
            # Compute velocity and acceleration
            new_velocity = (self.commanded_position - self.estimated_position) / self.time_delta if self.time_delta > 0 else 0
            self.acceleration = (new_velocity - self.velocity) / self.time_delta if self.time_delta > 0 else 0
            self.velocity = new_velocity
            
        
        # Update for next iteration
        self.previous_error = error
        self.estimated_position = self.commanded_position

        
        return self.commanded_position



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

# Initialize PID controllers for x and y axes
pid_x = PID(kp=.7, ki=0.05, kd=0.001, initial_position=x)
pid_y = PID(kp=.7, ki=0.05, kd=0.001, initial_position=y)


def calc_a_v(pid_x, pid_y):
    a = (pid_x.acceleration ** 2 + pid_y.acceleration ** 2) ** 0.5
    v = (pid_x.velocity ** 2 + pid_y.velocity ** 2) ** 0.5
    return a, v
    
use_pid = False;

while True:
    if uart.any:
        try:
            s = uart_readline(uart, 100)
            if s:
                s = s.decode().strip()
                x, y = map(int, s.split())
        except Exception as e:
            uart.write("error: " + str(e) + "\n")
           
    if use_pid:
        # Update PID controllers and get commanded positions
        commanded_x = pid_x.update(x)
        commanded_y = pid_y.update(y)

        a, v = calc_a_v(pid_x, pid_y)
    else:
        commanded_x = x
        commanded_y = y
        a = 0
        v = 0

        
        

    uart.write("cx=%4.1f tx=%4.1f cy=%4.1f ty=%4.1f a=%4.1F v=%4.1f\n"
               % (commanded_x, x, commanded_y, y, a, v) )
    
    # Move servos to commanded positions
    sx.write_angle(commanded_x)
    sy.write_angle(commanded_y)

    # Map to grid and update display
    px, py = map_xy_to_grid(commanded_x, commanded_y)
    display.clear()
    display.set_pixel(px, py, 9)


