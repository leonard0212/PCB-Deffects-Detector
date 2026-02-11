# ai_inference.py - Modul inferență AI cu YOLOv11
from ultralytics import YOLO
import cv2

class AIModel:
    def __init__(self, model_path, conf_thresh=0.5):
        print(f"[AI] Încărcare model: {model_path}...")
        self.model = YOLO(model_path)
        self.conf = conf_thresh
        print("[AI] Model încărcat!")

    def predict(self, frame):
        # Rulăm inferența
        results = self.model(frame, conf=self.conf, verbose=False)
        
        # Desenează automat cutiile și labels
        annotated_frame = results[0].plot()
        
        # Verificăm dacă avem defecte
        defect_found = False
        detections = []
        
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = self.model.names[cls_id]
                conf = float(box.conf[0])
                detections.append(f"{cls_name} ({conf:.2f})")
                defect_found = True
        
        print(f"[AI] Detectat: {len(detections)} defecte - {detections}")
        return annotated_frame, defect_found, detections
