# camera.py - Manager cameră video
import cv2
import time

class CameraManager:
    def __init__(self, index):
        self.current_index = index
        self.cap = cv2.VideoCapture(index)
        # Optimizare buffer pentru latență mică
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        
        if not self.cap.isOpened():
            print(f"[ERROR] Camera {index} not opened.")

    def get_frame(self):
        if not self.cap.isOpened():
            return None, False
        
        ret, frame = self.cap.read()
        if ret:
            # Redimensionare pentru performanță GUI
            frame = cv2.resize(frame, (640, 480))
        return frame, ret

    def release(self):
        self.cap.release()
