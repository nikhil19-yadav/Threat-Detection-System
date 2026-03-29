import cv2

cap = None

def start_camera():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)

def stop_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None

def process_frame():
    global cap

    if cap is None:
        return None

    ret, frame = cap.read()

    if not ret:
        return None

    return frame