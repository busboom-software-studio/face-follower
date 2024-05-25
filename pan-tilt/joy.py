import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check if there are any joysticks connected
if pygame.joystick.get_count() == 0:
    print("No joystick connected!")
    pygame.quit()
    sys.exit()


# Get the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick initialized: {joystick.get_name()}")

try:
    while True:
        # Process Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Read axis positions
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        # Print the position values
        print(f"X-axis: {axis_x:.2f}, Y-axis: {axis_y:.2f}")

        # Delay to limit the rate of print statements
        pygame.time.wait(100)

except KeyboardInterrupt:
    # Quit Pygame when the user interrupts the program
    pygame.quit()
    print("\nProgram terminated by user.")
