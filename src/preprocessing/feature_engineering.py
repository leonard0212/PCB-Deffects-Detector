# feature_engineering.py - Extragere și transformare features din imagini PCB
"""
Preprocesare – Feature Engineering.

Transformări aplicate imaginilor PCB:
  - Resize la dimensiunea standard (640x640)
  - Normalizare valori pixeli
  - Aplicare augmentări suplimentare (dacă e nevoie)
  - Extragere statistici imagine (pentru analiză)
"""

import os
import cv2
import numpy as np


def resize_image(image, target_size=(640, 640)):
    """Redimensionează imaginea la dimensiunea standard."""
    return cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)


def normalize_image(image):
    """Normalizează valorile pixelilor la intervalul [0, 1]."""
    return image.astype(np.float32) / 255.0


def compute_image_stats(image):
    """
    Calculează statistici descriptive pentru o imagine.
    
    Returns:
        dict: Media, deviația standard, histogramă per canal
    """
    stats = {
        "mean_b": float(np.mean(image[:, :, 0])),
        "mean_g": float(np.mean(image[:, :, 1])),
        "mean_r": float(np.mean(image[:, :, 2])),
        "std_b": float(np.std(image[:, :, 0])),
        "std_g": float(np.std(image[:, :, 1])),
        "std_r": float(np.std(image[:, :, 2])),
        "brightness": float(np.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))),
    }
    return stats


def apply_clahe(image, clip_limit=2.0, tile_size=(8, 8)):
    """
    Aplică CLAHE (Contrast Limited Adaptive Histogram Equalization).
    Util pentru imagini PCB cu iluminare neuniformă.
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge([l_clahe, a, b])
    return cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)


def extract_edges(image, low_threshold=50, high_threshold=150):
    """Extrage harta de margini Canny (util pentru detecția PCB în cadru)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, low_threshold, high_threshold)
    return edges


def process_image_pipeline(image, target_size=(640, 640), apply_enhancement=False):
    """
    Pipeline complet de preprocesare imagine.
    
    Args:
        image: Imaginea BGR originală
        target_size: Dimensiunea țintă
        apply_enhancement: Dacă se aplică CLAHE
    
    Returns:
        Imaginea preprocesată
    """
    processed = resize_image(image, target_size)
    
    if apply_enhancement:
        processed = apply_clahe(processed)
    
    return processed


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        img = cv2.imread(sys.argv[1])
        if img is not None:
            stats = compute_image_stats(img)
            print("Statistici imagine:")
            for k, v in stats.items():
                print(f"  {k}: {v:.2f}")
            
            processed = process_image_pipeline(img, apply_enhancement=True)
            cv2.imwrite("processed_output.jpg", processed)
            print("\nImaginea preprocesată salvată: processed_output.jpg")
    else:
        print("Utilizare: python feature_engineering.py <imagine.jpg>")
