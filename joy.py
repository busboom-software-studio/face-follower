import hid
import time
import datetime

def list_joysticks():
    devices = hid.enumerate()
    joystick_count = 0
    for device in devices:
        if device['interface_number'] == 1:
            joystick_count += 1
            print(f"Joystick {joystick_count}: {str(device)} {device['product_string']}")

def joystick_output(joystick_number):
    devices = hid.enumerate()
    joystick_count = 0
    for device in devices:
        if device['interface_number'] == 1:
            joystick_count += 1
            if joystick_count == joystick_number:
                joystick = hid.Device()
                joystick.open_path(device['path'])
                while True:
                    try:
                        data = joystick.read(64, timeout_ms=100)
                        if data:
                            print(f"{datetime.datetime.now()}: J{joystick_number}", end=' ')
                            for i, value in enumerate(data):
                                print(f"Axis {i}: {value}", end=' ')
                            print()
                    except KeyboardInterrupt:
                        joystick.close()
                        return

def main():
    while True:
        list_joysticks()
        devices = hid.enumerate()
        joystick_count = sum(1 for device in devices if device['interface_number'] == 1)
        if joystick_count == 0:
            print("No joysticks found.")
            return
        user_input = input("Enter a joystick number to see its output or 'q' to quit: ")
        if user_input.lower() == 'q':
            return
        elif user_input.isdigit():
            joystick_number = int(user_input)
            if joystick_number > joystick_count:
                print("Invalid joystick number.")
            else:
                joystick_output(joystick_number)

if __name__ == "__main__":
    main()
