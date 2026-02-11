# visualize.py - Generare grafice și vizualizări din rezultatele antrenării
"""
Modul 2 – Etape 5+6: Vizualizare rezultate antrenare și optimizare.

Generează:
  - Loss curves (train/val)
  - Metrici per epocă
  - Confusion matrix
  - Comparații între experimente
"""

import os
import sys
import json
import csv
import numpy as np

try:
    import matplotlib
    matplotlib.use('Agg')  # Backend non-interactiv
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("[WARN] matplotlib nu este instalat. Graficele nu vor fi generate.")


def load_training_history(csv_path):
    """Încarcă istoricul antrenării din CSV."""
    data = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key, value in row.items():
                key = key.strip()
                if key not in data:
                    data[key] = []
                try:
                    data[key].append(float(value))
                except ValueError:
                    data[key].append(value)
    return data


def plot_loss_curves(history, output_path):
    """Generează graficul loss curves (train vs validation)."""
    if not HAS_MPL:
        return
    
    epochs = history.get('epoch', range(len(history.get('train/box_loss', []))))
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Box Loss
    axes[0].plot(epochs, history['train/box_loss'], 'b-', label='Train', linewidth=1.5)
    axes[0].plot(epochs, history['val/box_loss'], 'r-', label='Validation', linewidth=1.5)
    axes[0].set_title('Box Loss', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoca')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Classification Loss
    axes[1].plot(epochs, history['train/cls_loss'], 'b-', label='Train', linewidth=1.5)
    axes[1].plot(epochs, history['val/cls_loss'], 'r-', label='Validation', linewidth=1.5)
    axes[1].set_title('Classification Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoca')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # DFL Loss
    axes[2].plot(epochs, history['train/dfl_loss'], 'b-', label='Train', linewidth=1.5)
    axes[2].plot(epochs, history['val/dfl_loss'], 'r-', label='Validation', linewidth=1.5)
    axes[2].set_title('DFL Loss', fontsize=14, fontweight='bold')
    axes[2].set_xlabel('Epoca')
    axes[2].set_ylabel('Loss')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[Viz] Loss curves salvate: {output_path}")


def plot_metrics_evolution(history, output_path):
    """Generează graficul evoluției metricilor."""
    if not HAS_MPL:
        return
    
    epochs = history.get('epoch', range(len(history.get('metrics/precision(B)', []))))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(epochs, history['metrics/precision(B)'], 'g-', label='Precision', linewidth=2)
    ax.plot(epochs, history['metrics/recall(B)'], 'b-', label='Recall', linewidth=2)
    ax.plot(epochs, history['metrics/mAP50(B)'], 'r-', label='mAP@50', linewidth=2)
    ax.plot(epochs, history['metrics/mAP50-95(B)'], 'm-', label='mAP@50-95', linewidth=2)
    
    ax.set_title('Evoluția Metricilor pe Parcursul Antrenării', fontsize=14, fontweight='bold')
    ax.set_xlabel('Epoca', fontsize=12)
    ax.set_ylabel('Valoare', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.05)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[Viz] Metrics evolution salvat: {output_path}")


def plot_learning_curves(history, output_path):
    """Generează learning curves finale."""
    if not HAS_MPL:
        return
    
    epochs = history.get('epoch', range(len(history.get('train/box_loss', []))))
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Total train loss
    train_total = [b + c + d for b, c, d in zip(
        history['train/box_loss'], history['train/cls_loss'], history['train/dfl_loss']
    )]
    val_total = [b + c + d for b, c, d in zip(
        history['val/box_loss'], history['val/cls_loss'], history['val/dfl_loss']
    )]
    
    axes[0, 0].plot(epochs, train_total, 'b-', label='Train Total Loss', linewidth=1.5)
    axes[0, 0].plot(epochs, val_total, 'r-', label='Val Total Loss', linewidth=1.5)
    axes[0, 0].set_title('Total Loss', fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Precision & Recall
    axes[0, 1].plot(epochs, history['metrics/precision(B)'], 'g-', label='Precision', linewidth=1.5)
    axes[0, 1].plot(epochs, history['metrics/recall(B)'], 'b-', label='Recall', linewidth=1.5)
    axes[0, 1].set_title('Precision & Recall', fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_ylim(0.5, 1.02)
    
    # mAP
    axes[1, 0].plot(epochs, history['metrics/mAP50(B)'], 'r-', label='mAP@50', linewidth=1.5)
    axes[1, 0].plot(epochs, history['metrics/mAP50-95(B)'], 'm-', label='mAP@50-95', linewidth=1.5)
    axes[1, 0].set_title('Mean Average Precision', fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_ylim(0, 1.05)
    
    # Learning Rate
    axes[1, 1].plot(epochs, history['lr/pg0'], 'k-', label='LR pg0', linewidth=1.5)
    axes[1, 1].set_title('Learning Rate Schedule', fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    for ax_row in axes:
        for ax in ax_row:
            ax.set_xlabel('Epoca')
    
    plt.suptitle('Learning Curves – YOLOv11n PCB Defect Detection', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[Viz] Learning curves salvate: {output_path}")


def generate_all_visualizations(history_csv, output_dir):
    """Generează toate graficele din istoricul antrenării."""
    os.makedirs(output_dir, exist_ok=True)
    
    history = load_training_history(history_csv)
    
    plot_loss_curves(history, os.path.join(output_dir, "loss_curve.png"))
    plot_metrics_evolution(history, os.path.join(output_dir, "metrics_evolution.png"))
    plot_learning_curves(history, os.path.join(output_dir, "learning_curves_final.png"))
    
    print(f"\n[Viz] Toate graficele generate în: {output_dir}")


if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    history_path = os.path.join(project_root, "results", "training_history.csv")
    output = os.path.join(project_root, "docs", "results")
    
    if os.path.exists(history_path):
        generate_all_visualizations(history_path, output)
    else:
        print(f"[ERROR] Nu s-a găsit: {history_path}")
