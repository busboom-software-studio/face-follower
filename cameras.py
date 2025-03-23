
import cv2
from matplotlib import pyplot as plt


def test_camera(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Cannot open camera {index}")
        return
    ret, frame = cap.read()

    if ret:
        print(f"Camera {index} is working.")
        display_frame(frame)
    else:
        print(f"Camera {index} is not working.")


        cap.release()

def display_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.imshow(frame)
    plt.axis('off')  # Turn off axis numbers and ticks
    plt.show()

test_camera(1)
