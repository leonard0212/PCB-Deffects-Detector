# debug_camera.py - Verificare camere disponibile
import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"[OK] Camera {i} available")
        cap.release()
    else:
        print(f"[X] Camera {i} NOT available")
