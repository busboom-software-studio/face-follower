import hid

def list_joysticks():
    # Get a list of all connected HID devices
    devices = hid.enumerate()

    # Filter the devices to only include joysticks
    joysticks = [device for device in devices if device['usage_page'] == 1 and device['usage'] == 4]

    # Print the details of each joystick
    for joystick in joysticks:
        print(f"Joystick: {joystick}")

# Call the function to list the joysticks
list_joysticks()