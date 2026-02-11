# data_cleaner.py - Curățare și validare date PCB
"""
Preprocesare – Curățare date brute.

Funcționalități:
  - Verificare integritate imagini
  - Eliminare imagini corupte sau prea mici
  - Normalizare dimensiuni
  - Verificare adnotări YOLO (format corect)
"""

import os
import glob
import cv2
import shutil


def validate_image(img_path, min_size=32):
    """
    Verifică dacă o imagine este validă.
    
    Args:
        img_path: Calea imaginii
        min_size: Dimensiunea minimă (pixeli)
    
    Returns:
        bool: True dacă imaginea e validă
    """
    try:
        img = cv2.imread(img_path)
        if img is None:
            return False
        h, w = img.shape[:2]
        if h < min_size or w < min_size:
            return False
        return True
    except Exception:
        return False


def validate_label(label_path):
    """
    Verifică dacă un fișier de adnotări YOLO este valid.
    Format așteptat per linie: class_id x_center y_center width height
    """
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                return False
            cls_id = int(parts[0])
            coords = [float(x) for x in parts[1:]]
            # Verificare bounds [0, 1]
            if any(c < 0 or c > 1 for c in coords):
                return False
        return True
    except Exception:
        return False


def clean_dataset(input_dir, output_dir, img_ext=('.jpg', '.png', '.jpeg')):
    """
    Curăță dataset-ul: elimină imagini corupte și adnotări invalide.
    
    Args:
        input_dir: Director cu imagini + labels
        output_dir: Director curățat
        img_ext: Extensii imagini acceptate
    """
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels'), exist_ok=True)
    
    img_dir = os.path.join(input_dir, 'images')
    lbl_dir = os.path.join(input_dir, 'labels')
    
    valid_count = 0
    invalid_count = 0
    
    for ext in img_ext:
        for img_path in glob.glob(os.path.join(img_dir, f'*{ext}')):
            fname = os.path.splitext(os.path.basename(img_path))[0]
            label_path = os.path.join(lbl_dir, f'{fname}.txt')
            
            # Verificare imagine
            if not validate_image(img_path):
                invalid_count += 1
                print(f"[SKIP] Imagine invalidă: {img_path}")
                continue
            
            # Verificare label (dacă există)
            if os.path.exists(label_path) and not validate_label(label_path):
                invalid_count += 1
                print(f"[SKIP] Label invalid: {label_path}")
                continue
            
            # Copiere fișiere valide
            shutil.copy2(img_path, os.path.join(output_dir, 'images', os.path.basename(img_path)))
            if os.path.exists(label_path):
                shutil.copy2(label_path, os.path.join(output_dir, 'labels', f'{fname}.txt'))
            
            valid_count += 1
    
    print(f"\n[Clean] Rezultat: {valid_count} valide, {invalid_count} eliminate")
    return valid_count, invalid_count


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        clean_dataset(sys.argv[1], sys.argv[2])
    else:
        print("Utilizare: python data_cleaner.py <input_dir> <output_dir>")
