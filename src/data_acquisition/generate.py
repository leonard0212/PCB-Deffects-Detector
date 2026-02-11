# generate.py - Generare date sintetice PCB cu defecte
"""
Modul 1 – Generare date sintetice suplimentare.

Script auxiliar pentru generarea de imagini sintetice de PCB-uri cu defecte controlate.
Datele principale (~400 imagini) au fost colectate în vara 2025 în cadrul unui internship
la Steinel Electronic, Curtea de Argeș. Acest script poate fi folosit pentru a completa
dataset-ul cu date sintetice suplimentare dacă este necesar.

Clase de defecte:
  - missing_hole: Lipsa găurii de montaj
  - mouse_bite: Deteriorare margine PCB
  - open_circuit: Circuit deschis (întrerupere pistă)
  - short: Scurtcircuit între piste
  - spur: Proeminență pe pistă
  - spurious_copper: Cupru rezidual nedorit

Output: Imagini + adnotări format YOLO
"""

import os
import sys
import cv2
import numpy as np
import random
from datetime import datetime


# Clase de defecte
DEFECT_CLASSES = {
    0: "missing_hole",
    1: "mouse_bite",
    2: "open_circuit",
    3: "short",
    4: "spur",
    5: "spurious_copper",
}

# Culori tipice PCB
PCB_COLORS = [
    (0, 100, 0),     # Verde clasic
    (0, 80, 0),      # Verde închis
    (20, 60, 120),   # Maro
    (100, 50, 0),    # Albastru
]

IMG_SIZE = 640


def generate_pcb_background(size=IMG_SIZE):
    """Generează un fundal de PCB sintetic."""
    color = random.choice(PCB_COLORS)
    bg = np.full((size, size, 3), color, dtype=np.uint8)
    
    # Adaugă textura tipică PCB (linii/piste)
    num_traces = random.randint(5, 15)
    for _ in range(num_traces):
        pt1 = (random.randint(0, size), random.randint(0, size))
        pt2 = (random.randint(0, size), random.randint(0, size))
        thickness = random.randint(1, 4)
        trace_color = (180, 180, 140)  # Cupru
        cv2.line(bg, pt1, pt2, trace_color, thickness)
    
    # Adaugă pads (puncte de lipire)
    num_pads = random.randint(5, 20)
    for _ in range(num_pads):
        center = (random.randint(30, size-30), random.randint(30, size-30))
        radius = random.randint(3, 8)
        cv2.circle(bg, center, radius, (200, 200, 180), -1)
    
    # Adaugă zgomot ușor
    noise = np.random.randint(-10, 10, bg.shape, dtype=np.int16)
    bg = np.clip(bg.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return bg


def add_defect(image, defect_class):
    """
    Adaugă un defect sintetic pe imagine.
    
    Returns:
        image: Imaginea cu defect
        bbox: (x_center, y_center, width, height) normalizat [0,1]
    """
    h, w = image.shape[:2]
    
    # Zonă aleatoare pentru defect
    def_w = random.randint(20, 80)
    def_h = random.randint(20, 80)
    x = random.randint(def_w, w - def_w)
    y = random.randint(def_h, h - def_h)
    
    if defect_class == 0:  # missing_hole
        radius = random.randint(5, 15)
        cv2.circle(image, (x, y), radius, (30, 30, 30), -1)
        def_w = def_h = radius * 2
        
    elif defect_class == 1:  # mouse_bite
        for _ in range(random.randint(3, 7)):
            dx = random.randint(-15, 15)
            dy = random.randint(-15, 15)
            r = random.randint(2, 5)
            cv2.circle(image, (x + dx, y + dy), r, (30, 30, 30), -1)
        
    elif defect_class == 2:  # open_circuit
        pt1 = (x - def_w // 2, y)
        pt2 = (x + def_w // 2, y)
        cv2.line(image, pt1, pt2, (30, 30, 30), 3)
        
    elif defect_class == 3:  # short
        pt1 = (x, y - def_h // 2)
        pt2 = (x + random.randint(10, 30), y + def_h // 2)
        cv2.line(image, pt1, pt2, (180, 180, 140), random.randint(2, 5))
        
    elif defect_class == 4:  # spur
        for _ in range(random.randint(2, 5)):
            dx = random.randint(-20, 20)
            dy = random.randint(-20, 20)
            cv2.line(image, (x, y), (x + dx, y + dy), (180, 180, 140), 2)
        
    elif defect_class == 5:  # spurious_copper
        pts = np.array([(x + random.randint(-20, 20), y + random.randint(-20, 20))
                        for _ in range(random.randint(4, 8))], np.int32)
        cv2.fillPoly(image, [pts], (180, 180, 140))
    
    # Bounding box normalizat
    x_center = x / w
    y_center = y / h
    bbox_w = def_w / w
    bbox_h = def_h / h
    
    return image, (x_center, y_center, bbox_w, bbox_h)


def generate_dataset(output_dir, num_images=100, defects_per_image=(1, 3)):
    """
    Generează un dataset complet de imagini PCB cu defecte.
    
    Args:
        output_dir: Director de ieșire
        num_images: Numărul de imagini de generat
        defects_per_image: (min, max) defecte per imagine
    """
    images_dir = os.path.join(output_dir, 'images')
    labels_dir = os.path.join(output_dir, 'labels')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    
    for i in range(num_images):
        # Generează PCB
        img = generate_pcb_background()
        
        # Adaugă defecte
        num_defects = random.randint(*defects_per_image)
        labels = []
        
        for _ in range(num_defects):
            cls_id = random.randint(0, len(DEFECT_CLASSES) - 1)
            img, bbox = add_defect(img, cls_id)
            labels.append(f"{cls_id} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}")
        
        # Salvare
        img_name = f"pcb_gen_{i:05d}.jpg"
        cv2.imwrite(os.path.join(images_dir, img_name), img)
        
        lbl_name = f"pcb_gen_{i:05d}.txt"
        with open(os.path.join(labels_dir, lbl_name), 'w') as f:
            f.write('\n'.join(labels))
        
        if (i + 1) % 50 == 0:
            print(f"[Generate] {i + 1}/{num_images} imagini generate...")
    
    print(f"\n[Generate] Dataset generat: {num_images} imagini în {output_dir}")
    print(f"  - Imagini: {images_dir}")
    print(f"  - Labels:  {labels_dir}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generare date sintetice PCB')
    parser.add_argument('--output', default='../../data/generated', help='Director output')
    parser.add_argument('--count', type=int, default=100, help='Număr imagini')
    args = parser.parse_args()
    
    generate_dataset(args.output, args.count)
