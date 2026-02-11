# optimize.py - Experimente optimizare hiperparametri
"""
Modul 2 – Etapa 6: Optimizare model prin experimente sistematice.

Compară diferite configurații de hiperparametri:
  - Learning rate
  - Batch size
  - Augmentări
  - Arhitecturi (nano vs small)
  
Salvează rezultatele în optimization_experiments.csv
"""

import os
import sys
import csv
import json
from datetime import datetime
from ultralytics import YOLO


# Experimente de optimizare
EXPERIMENTS = [
    {
        "name": "baseline",
        "model": "yolo11n.pt",
        "lr0": 0.01,
        "batch": 16,
        "epochs": 100,
        "patience": 25,
        "mosaic": 1.0,
        "erasing": 0.4,
        "notes": "Configurație baseline originală"
    },
    {
        "name": "lr_lower",
        "model": "yolo11n.pt",
        "lr0": 0.005,
        "batch": 16,
        "epochs": 100,
        "patience": 25,
        "mosaic": 1.0,
        "erasing": 0.4,
        "notes": "Learning rate redus la 0.005"
    },
    {
        "name": "batch_32",
        "model": "yolo11n.pt",
        "lr0": 0.01,
        "batch": 32,
        "epochs": 100,
        "patience": 25,
        "mosaic": 1.0,
        "erasing": 0.4,
        "notes": "Batch size crescut la 32"
    },
    {
        "name": "augment_heavy",
        "model": "yolo11n.pt",
        "lr0": 0.01,
        "batch": 16,
        "epochs": 100,
        "patience": 25,
        "mosaic": 1.0,
        "erasing": 0.6,
        "mixup": 0.15,
        "notes": "Augmentări mai agresive (erasing=0.6, mixup=0.15)"
    },
]


def run_experiment(experiment, data_yaml, project_dir):
    """Rulează un singur experiment de optimizare."""
    exp_name = experiment["name"]
    print(f"\n{'='*60}")
    print(f"EXPERIMENT: {exp_name}")
    print(f"Note: {experiment.get('notes', '')}")
    print(f"{'='*60}")
    
    model = YOLO(experiment["model"])
    
    results = model.train(
        data=data_yaml,
        epochs=experiment.get("epochs", 100),
        patience=experiment.get("patience", 25),
        batch=experiment.get("batch", 16),
        imgsz=640,
        lr0=experiment.get("lr0", 0.01),
        mosaic=experiment.get("mosaic", 1.0),
        erasing=experiment.get("erasing", 0.4),
        mixup=experiment.get("mixup", 0.0),
        project=project_dir,
        name=exp_name,
        exist_ok=True,
        plots=True,
        save=True,
    )
    
    return results


def run_all_experiments(data_yaml, project_dir=None):
    """Rulează toate experimentele și salvează comparația."""
    if project_dir is None:
        project_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', 'results'
        ))
    
    results_csv = os.path.join(project_dir, "optimization_experiments.csv")
    
    all_results = []
    for exp in EXPERIMENTS:
        try:
            result = run_experiment(exp, data_yaml, project_dir)
            all_results.append({
                "experiment": exp["name"],
                "notes": exp.get("notes", ""),
                "lr0": exp.get("lr0"),
                "batch": exp.get("batch"),
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            all_results.append({
                "experiment": exp["name"],
                "notes": exp.get("notes", ""),
                "lr0": exp.get("lr0"),
                "batch": exp.get("batch"),
                "status": f"error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
            })
    
    # Salvare CSV
    if all_results:
        keys = all_results[0].keys()
        with open(results_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_results)
        print(f"\nRezultate salvate: {results_csv}")
    
    return all_results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    else:
        print("Utilizare: python optimize.py <data.yaml>")
        sys.exit(1)
    
    run_all_experiments(data_path)
