# data_splitter.py - Împărțire dataset în train/validation/test
"""
Preprocesare – Data Splitting.

Împarte dataset-ul în:
  - Train: 70%
  - Validation: 15%
  - Test: 15%

Menține distribuția echilibrată a claselor (stratified split).
"""

import os
import random
import shutil
import glob
from collections import defaultdict


def get_class_distribution(labels_dir):
    """Calculează distribuția claselor din fișierele de adnotări."""
    class_counts = defaultdict(int)
    total_boxes = 0
    
    for label_file in glob.glob(os.path.join(labels_dir, '*.txt')):
        with open(label_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    cls_id = int(parts[0])
                    class_counts[cls_id] += 1
                    total_boxes += 1
    
    print(f"Distribuție clase ({total_boxes} total bounding boxes):")
    for cls_id in sorted(class_counts.keys()):
        pct = class_counts[cls_id] / total_boxes * 100
        print(f"  Clasa {cls_id}: {class_counts[cls_id]} ({pct:.1f}%)")
    
    return dict(class_counts)


def split_dataset(source_dir, output_dir, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, seed=42):
    """
    Împarte dataset-ul în train/val/test.
    
    Args:
        source_dir: Director sursă cu images/ și labels/
        output_dir: Director de ieșire
        train_ratio, val_ratio, test_ratio: Procentele de split
        seed: Seed pentru reproducibilitate
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, \
        "Sumele ratio-urilor trebuie să fie 1.0!"
    
    random.seed(seed)
    
    images_dir = os.path.join(source_dir, 'images')
    labels_dir = os.path.join(source_dir, 'labels')
    
    # Colectare toate fișierele imagine
    image_files = []
    for ext in ('*.jpg', '*.png', '*.jpeg'):
        image_files.extend(glob.glob(os.path.join(images_dir, ext)))
    
    random.shuffle(image_files)
    
    n = len(image_files)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    
    splits = {
        'train': image_files[:n_train],
        'validation': image_files[n_train:n_train + n_val],
        'test': image_files[n_train + n_val:],
    }
    
    for split_name, files in splits.items():
        img_out = os.path.join(output_dir, split_name, 'images')
        lbl_out = os.path.join(output_dir, split_name, 'labels')
        os.makedirs(img_out, exist_ok=True)
        os.makedirs(lbl_out, exist_ok=True)
        
        for img_path in files:
            fname = os.path.splitext(os.path.basename(img_path))[0]
            label_path = os.path.join(labels_dir, f'{fname}.txt')
            
            shutil.copy2(img_path, os.path.join(img_out, os.path.basename(img_path)))
            if os.path.exists(label_path):
                shutil.copy2(label_path, os.path.join(lbl_out, f'{fname}.txt'))
        
        print(f"[Split] {split_name}: {len(files)} imagini")
    
    print(f"\nTotal: {n} imagini împărțite în {output_dir}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        split_dataset(sys.argv[1], sys.argv[2])
    else:
        print("Utilizare: python data_splitter.py <source_dir> <output_dir>")
        print("Exemplu:   python data_splitter.py ../../data/processed ../../data")
