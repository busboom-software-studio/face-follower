import time
import serial
from simple_pid import PID
import struct



class PTServo:
    def __init__(self, serial_port, baud_rate):
        self.x = 90
        self.y = 90
        
        self.pid_y = PID(Kp=2, Ki=0.01, Kd=0.5, setpoint=0)
        self.pid_x = PID(Kp=3, Ki=0.01, Kd=0.5, setpoint=0)
        
        try:
            self.ser = serial.Serial(serial_port, baud_rate)
            self.ser.timeout = 0
            print(f"Opened serial port {serial_port}")
        except serial.SerialException:
            self.ser = None
            print(f"Could not open serial port {serial_port}, outputting to stdout")
            
        self.move_a(90, 180)


    def update_angles(self, centroid):
    
        y = self.pid_y(centroid[1]) 
        x = self.pid_x(centroid[0]) 
        
        print(f"x={round(x)}, y={round(y)}")
    
        self.move_r(-x , y)    
        


class PTServoMB(PTServo):

   
    def move_a(self, x, y):
        message = f"a {x} {y}\n"\
            
        self.ser.write(message.encode())
        
    def move_r(self, x, y):
        message = f"r {int(x)} {int(y)}\n"\
            
        self.ser.write(message.encode())
        
    def get_status(self):
        o = ""
        while self.ser.in_waiting > 0:
            o += self.ser.read(self.ser.in_waiting).decode()
            
        if 'Traceback' in o:
            raise Exception(o)
        return o
    

class PTServoArduino(PTServo):


    def check_status(self):
        
        self.send_angles(ord('?'), 0, 0)
        time.sleep(0.1)
        return self.get_status()

    def move_a(self, x, y):
        
        self.send_angles(ord('a'), x, y)
        
    def move_r(self, x, y):
        
        self.send_angles(ord('r'), x, y)

    def send_angles(self, code: int, angle1 : float, angle2: float ):
        """
        Sends angles to a serial port.
        
        Args:
            ser: The serial port object.
            angle1 (float): The first angle to send.
            angle2 (float): The second angle to send.
        
        Returns:
            str: The response received from the serial port.
        """
        # Convert angles to 32-bit integers
        angle1 = max(int(angle1 * 10000), 1)
        angle2 = max(int(angle2 * 10000), 1)
        
        assert code != 0, "Code cannot be 0"
        
        data = struct.pack('<iiBB', angle1, angle2, code, 0)
  
        self.ser.write(data)

        
    def get_status(self):
        o = ""
        while self.ser.in_waiting > 0:
            o += self.ser.read(self.ser.in_waiting).decode()
            
        return o
            
        
        
    
