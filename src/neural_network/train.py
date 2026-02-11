# train.py - Script antrenare model YOLOv11 pe dataset PCB
"""
Modul 2 – Etapa 5: Antrenare model pe dataset de defecte PCB.

Folosește YOLOv11n pretrained pe COCO, fine-tuned pe dataset-ul PCB
cu 6 clase de defecte. Antrenarea salvează:
  - Modelul best (best.pt)
  - Istoricul antrenării (CSV)
  - Metrici pe validation set
"""

import os
import sys
import yaml
from ultralytics import YOLO

# Configurare antrenare
TRAIN_CONFIG = {
    "model": "yolo11n.pt",
    "epochs": 100,
    "patience": 25,
    "batch": 16,
    "imgsz": 640,
    "optimizer": "auto",
    "lr0": 0.01,
    "lrf": 0.01,
    "momentum": 0.937,
    "weight_decay": 0.0005,
    "warmup_epochs": 3.0,
    "warmup_momentum": 0.8,
    "cos_lr": False,
    "close_mosaic": 10,
    "amp": True,
    "plots": True,
    "save": True,
    "val": True,
    "deterministic": True,
    "seed": 0,
    # Augmentări
    "hsv_h": 0.015,
    "hsv_s": 0.7,
    "hsv_v": 0.4,
    "flipud": 0.0,
    "fliplr": 0.5,
    "mosaic": 1.0,
    "mixup": 0.0,
    "scale": 0.5,
    "translate": 0.1,
    "erasing": 0.4,
}


def train(data_yaml_path, project_dir=None, run_name="model_pcb"):
    """
    Lansează antrenarea modelului YOLOv11n.
    
    Args:
        data_yaml_path (str): Calea către data.yaml al dataset-ului
        project_dir (str): Directorul unde se salvează rezultatele
        run_name (str): Numele experimentului
    """
    if project_dir is None:
        project_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'results'
        ))
    
    # Inițializare model pretrained
    model = YOLO(TRAIN_CONFIG["model"])
    
    # Lansare antrenare
    results = model.train(
        data=data_yaml_path,
        epochs=TRAIN_CONFIG["epochs"],
        patience=TRAIN_CONFIG["patience"],
        batch=TRAIN_CONFIG["batch"],
        imgsz=TRAIN_CONFIG["imgsz"],
        optimizer=TRAIN_CONFIG["optimizer"],
        lr0=TRAIN_CONFIG["lr0"],
        lrf=TRAIN_CONFIG["lrf"],
        momentum=TRAIN_CONFIG["momentum"],
        weight_decay=TRAIN_CONFIG["weight_decay"],
        warmup_epochs=TRAIN_CONFIG["warmup_epochs"],
        warmup_momentum=TRAIN_CONFIG["warmup_momentum"],
        cos_lr=TRAIN_CONFIG["cos_lr"],
        close_mosaic=TRAIN_CONFIG["close_mosaic"],
        amp=TRAIN_CONFIG["amp"],
        plots=TRAIN_CONFIG["plots"],
        save=TRAIN_CONFIG["save"],
        val=TRAIN_CONFIG["val"],
        deterministic=TRAIN_CONFIG["deterministic"],
        seed=TRAIN_CONFIG["seed"],
        hsv_h=TRAIN_CONFIG["hsv_h"],
        hsv_s=TRAIN_CONFIG["hsv_s"],
        hsv_v=TRAIN_CONFIG["hsv_v"],
        flipud=TRAIN_CONFIG["flipud"],
        fliplr=TRAIN_CONFIG["fliplr"],
        mosaic=TRAIN_CONFIG["mosaic"],
        mixup=TRAIN_CONFIG["mixup"],
        scale=TRAIN_CONFIG["scale"],
        translate=TRAIN_CONFIG["translate"],
        erasing=TRAIN_CONFIG["erasing"],
        project=project_dir,
        name=run_name,
        exist_ok=True,
    )
    
    print(f"\n{'='*50}")
    print(f"Antrenare completă!")
    print(f"Rezultate salvate în: {project_dir}/{run_name}")
    print(f"{'='*50}")
    
    return results


if __name__ == "__main__":
    # Exemplu utilizare:
    # python train.py path/to/data.yaml
    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    else:
        data_path = "data.yaml"
        print(f"[INFO] Nu s-a specificat data.yaml, se folosește: {data_path}")
    
    train(data_path)
