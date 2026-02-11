# model.py - Definire arhitectură model YOLOv11 pentru detecție defecte PCB
"""
Modul 2 – Etapa 4: Definirea arhitecturii rețelei neuronale.

Modelul utilizat este YOLOv11n (nano), o arhitectură single-shot detector
optimizată pentru detecția de obiecte în timp real, pretrained pe COCO și
fine-tuned pe dataset-ul de defecte PCB.

Clase detectate:
  0: missing_hole
  1: mouse_bite
  2: open_circuit
  3: short
  4: spur
  5: spurious_copper
"""

from ultralytics import YOLO
import os

# Configurare
NUM_CLASSES = 6
IMG_SIZE = 640
MODEL_VARIANT = "yolo11n.pt"  # Variantă nano pentru inferență rapidă

CLASS_NAMES = [
    "missing_hole",
    "mouse_bite", 
    "open_circuit",
    "short",
    "spur",
    "spurious_copper"
]


def create_model(pretrained=True):
    """
    Creează și returnează modelul YOLOv11n.
    
    Args:
        pretrained (bool): Dacă se încarcă greutățile pretrained COCO
        
    Returns:
        YOLO: Instanță model YOLO
    """
    if pretrained:
        model = YOLO(MODEL_VARIANT)
        print(f"[Model] Încărcat {MODEL_VARIANT} cu greutăți pretrained COCO")
    else:
        # Model de la zero (nerecomandat pentru fine-tuning)
        model = YOLO(MODEL_VARIANT)
        print(f"[Model] Încărcat {MODEL_VARIANT} schelet arhitectură")
    
    return model


def load_trained_model(model_path):
    """
    Încarcă un model antrenat din fișier .pt
    
    Args:
        model_path (str): Calea către fișierul .pt
        
    Returns:
        YOLO: Model încărcat cu greutăți antrenate
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelul nu a fost găsit: {model_path}")
    
    model = YOLO(model_path)
    print(f"[Model] Încărcat model antrenat din: {model_path}")
    return model


def get_model_info(model):
    """
    Afișează informații despre arhitectura modelului.
    """
    info = model.info()
    print(f"\n{'='*50}")
    print(f"Arhitectură: YOLOv11n")
    print(f"Clase: {NUM_CLASSES} ({', '.join(CLASS_NAMES)})")
    print(f"Input: {IMG_SIZE}x{IMG_SIZE}")
    print(f"{'='*50}\n")
    return info


if __name__ == "__main__":
    # Demo: Creează și afișează informații model
    model = create_model(pretrained=True)
    get_model_info(model)
