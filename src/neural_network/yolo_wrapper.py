from ultralytics import YOLO
import os

class PCBModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                print(f"[NeuralNetwork] Încărcare model: {self.model_path}")
                self.model = YOLO(self.model_path)
            except Exception as e:
                print(f"[Eroare] Model incompatibil: {e}")
        else:
            print(f"[Eroare] Fișierul {self.model_path} nu există.")

    def predict(self, image, confidence=0.25):
        if self.model is None:
            return None
        # Rulăm inferența
        results = self.model(image, conf=confidence)
        return results[0]
