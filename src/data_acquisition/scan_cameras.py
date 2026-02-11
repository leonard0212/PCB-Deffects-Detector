# scan_cameras.py - Scanare camere disponibile
import cv2
import time

print("[DEBUG] Scanning for available cameras...")
print()

for i in range(5):
    print(f"Testing camera {i}...", end=" ")
    cap = cv2.VideoCapture(i)
    
    if not cap.isOpened():
        print("[FAIL] Cannot open")
        continue
    
    print("[OK] Opened, ", end="")
    
    ret, frame = cap.read()
    if ret and frame is not None:
        h, w = frame.shape[:2]
        print(f"Frame: {w}x{h} [WORKING]")
    else:
        print("[FAIL] No frame")
    
    cap.release()
    time.sleep(0.5)

print()
print("[INFO] Check which index works and update CAMERA_INDEX in config.py")
