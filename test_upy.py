"""Send commands to the Micropython controller over serial."""
from ptservo import PTServoMB, PTServoArduino
import time
import math

from pynput import keyboard

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

def kbd_move():
    """Yields x and y values from keyboard input."""
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.esc:
                return 
            elif event.key == keyboard.Key.up:
                yield 0, 5
            elif event.key == keyboard.Key.down:
                yield 0, -5
            elif event.key == keyboard.Key.right:
                yield 5, 0
            elif event.key == keyboard.Key.left:
                yield -5, 0

def test():
    #pt_servo = PTServoMB('/dev/tty.usbmodem2212202', 115200)
    pt_servo = PTServoArduino('/dev/tty.usbmodem2212201', 115200)
    generator = flex()

    for x, y in generator:
        pt_servo.move_r(x, y)
        print(pt_servo.get_status())
        time.sleep(0.05)

if __name__ == "__main__":
    test()
