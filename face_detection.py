import cv2 # type: ignore
import time

# Load Haar cascade once
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_face_fast(cap):
    """
    Reads a frame and detects a face quickly.
    Returns True if a face is detected.
    """
    ret, frame = cap.read()
    if not ret or frame is None:
        return False

    # Resize for faster processing (optional)
    small_frame = cv2.resize(frame, (320, 240))

    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(30, 30)
    )

    return len(faces) > 0

def face_detection():
    print("Baymax: Starting vision check...")
    cap = cv2.VideoCapture(0)

    WAIT_TIME = 5  # seconds
    start_time = time.time()
    # Try reading up to 30 frames to find a face
    while time.time() - start_time < WAIT_TIME:
        for _ in range(30):
            if detect_face_fast(cap):
                print("Baymax: Face detected!")
                cap.release()
                return True

    print("Baymax: No face found.")
    cap.release()

if __name__ == "__main__":
    face_detection()