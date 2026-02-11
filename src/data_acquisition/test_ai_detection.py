# test_ai_detection.py - Test inferență AI pe frame cameră
import cv2
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from ai_inference import AIModel
from config import MODEL_PATH, CONFIDENCE_THRESHOLD

# Inițializare model
ai = AIModel(MODEL_PATH, CONFIDENCE_THRESHOLD)

# Citire frame de la cameră
cap = cv2.VideoCapture(1)
ret, frame = cap.read()

if ret:
    print(f"Frame citit: {frame.shape}")
    
    # Test predicție
    annotated_frame, defect_found, detections = ai.predict(frame)
    
    print(f"\nRezultat:")
    print(f"  Defect găsit: {defect_found}")
    print(f"  Detecții: {detections}")
    print(f"  Număr detecții: {len(detections)}")
    
    # Salvare imagine pentru inspecție
    cv2.imwrite("test_detection_result.jpg", annotated_frame)
    print(f"\nImaginea a fost salvată ca 'test_detection_result.jpg'")
    
    # Afișare imagine
    cv2.imshow("Detectie AI", annotated_frame)
    print("\nApasă orice tastă pentru a închide...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Nu s-a putut citi frame de la cameră!")

cap.release()
