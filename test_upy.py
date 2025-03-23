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
       
        for x,y in [(0,0), (0,180), (180,180), (180,0), (180, 180), (0,0)]:
            
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
    
    for i in range(10):
        #r = pt_servo.check_status().strip()
        #print(f"?: {i} '{r}'")
        r = pt_servo.get_status().strip()
        if r == 'ready.':
            break
        time.sleep(1)
    
    generator = flex()

    print(pt_servo.get_status())
    print('='*20) 
    for x, y in generator:
        print('-'*20)
        pt_servo.move_a(x, y)
        time.sleep(1)
        print(pt_servo.get_status())
        

if __name__ == "__main__":
    test()
