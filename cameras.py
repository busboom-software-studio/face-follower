import cv2
from matplotlib import pyplot as plt


def list_cameras(max_index=5):
    available_cameras = []
    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available_cameras.append(index)
            cap.release()
    return available_cameras


def test_camera(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Cannot open camera {index}")
        return
    ret, frame = cap.read()

    if ret:
        print(f"Camera {index} is working.")
        display_frame(frame)
        print("\nTo get a handle on this camera in your Python code, use:")
        print(f"cap = cv2.VideoCapture({index})")
    else:
        print(f"Camera {index} is not working.")
    cap.release()


def display_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.imshow(frame)
    plt.axis('off')  # Turn off axis numbers and ticks
    plt.show()


def main():
    print("Scanning for available cameras...")
    cameras = list_cameras()
    if not cameras:
        print("No cameras found.")
        return

    print("Available cameras:")
    for i, cam in enumerate(cameras):
        print(f"{i}: Camera {cam}")

    try:
        selection = int(input("Select a camera by entering its number: "))
        if 0 <= selection < len(cameras):
            test_camera(cameras[selection])
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
