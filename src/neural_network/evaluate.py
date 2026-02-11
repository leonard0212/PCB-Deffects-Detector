# evaluate.py - Evaluare model pe test set
"""
Modul 2 – Etapa 5: Evaluare metrici pe test set.

Calculează și salvează:
  - Precision, Recall, mAP@50, mAP@50-95
  - Confusion Matrix
  - Metrici per clasă
"""

import os
import sys
import json
from ultralytics import YOLO


def evaluate_model(model_path, data_yaml_path, output_dir=None):
    """
    Evaluează modelul pe dataset și salvează metricile.
    
    Args:
        model_path (str): Calea către modelul .pt
        data_yaml_path (str): Calea către data.yaml
        output_dir (str): Director pentru salvare rezultate
    """
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'results'
        ))
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Încarcă model
    model = YOLO(model_path)
    
    # Rulează evaluare
    metrics = model.val(data=data_yaml_path, imgsz=640, plots=True)
    
    # Extrage metrici
    results = {
        "model": os.path.basename(model_path),
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
        "map50": float(metrics.box.map50),
        "map50-95": float(metrics.box.map),
        "num_classes": len(metrics.box.ap),
    }
    
    # Per-class metrics
    class_names = model.names
    per_class = {}
    for i, (p, r, ap50, ap) in enumerate(zip(
        metrics.box.p, metrics.box.r, metrics.box.ap50, metrics.box.ap
    )):
        name = class_names.get(i, f"class_{i}")
        per_class[name] = {
            "precision": float(p),
            "recall": float(r),
            "ap50": float(ap50),
            "ap50-95": float(ap)
        }
    results["per_class"] = per_class
    
    # Salvare
    output_path = os.path.join(output_dir, "test_metrics.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"\n{'='*50}")
    print(f"REZULTATE EVALUARE")
    print(f"{'='*50}")
    print(f"Precision:  {results['precision']:.4f}")
    print(f"Recall:     {results['recall']:.4f}")
    print(f"mAP@50:     {results['map50']:.4f}")
    print(f"mAP@50-95:  {results['map50-95']:.4f}")
    print(f"\nMetrici salvate: {output_path}")
    print(f"{'='*50}")
    
    return results


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        model_p = sys.argv[1]
        data_p = sys.argv[2]
    else:
        print("Utilizare: python evaluate.py <model.pt> <data.yaml>")
        print("Exemplu:   python evaluate.py ../../models/pcb_model.pt data.yaml")
        sys.exit(1)
    
    evaluate_model(model_p, data_p)
