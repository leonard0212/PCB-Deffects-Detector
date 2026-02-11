# combine_datasets.py - Combinare date originale cu date externe
"""
Preprocesare – Combinare datasets.

Combină:
  - Date proprii (~400 imagini colectate la Steinel Electronic, vara 2025) din data/generated/
  - Date externe (din data/raw/)
  
Asigură:
  - Format unificat YOLO (images/ + labels/)
  - Eliminare duplicate
  
Notă: În antrenarea principală, datele proprii reprezintă ~3.6% din total (~400 din ~11.000).
S-a optat pentru această proporție în favoarea calității antrenării.
În cadrul internship-ului, s-a realizat și o antrenare pe ~1000 imagini (~40% date proprii).
"""

import os
import shutil
import glob
import hashlib


def file_hash(filepath):
    """Calculează hash SHA256 pentru detectarea duplicatelor."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def combine_datasets(generated_dir, external_dir, output_dir, min_original_ratio=0.036):
    """
    Combină date proprii cu date externe.
    
    Args:
        generated_dir: Director cu date proprii (colectate la Steinel Electronic)
        external_dir: Director cu date externe (raw)
        output_dir: Director output combinat
        min_original_ratio: Procentul minim de date proprii (default ~3.6%)
    """
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels'), exist_ok=True)
    
    seen_hashes = set()
    copied_original = 0
    copied_external = 0
    duplicates = 0
    
    # 1. Copiere date proprii (Steinel Electronic)
    gen_images = os.path.join(generated_dir, 'images')
    gen_labels = os.path.join(generated_dir, 'labels')
    
    if os.path.exists(gen_images):
        for img_path in glob.glob(os.path.join(gen_images, '*.*')):
            h = file_hash(img_path)
            if h in seen_hashes:
                duplicates += 1
                continue
            seen_hashes.add(h)
            
            fname = os.path.basename(img_path)
            stem = os.path.splitext(fname)[0]
            
            shutil.copy2(img_path, os.path.join(output_dir, 'images', f'gen_{fname}'))
            label_path = os.path.join(gen_labels, f'{stem}.txt')
            if os.path.exists(label_path):
                shutil.copy2(label_path, os.path.join(output_dir, 'labels', f'gen_{stem}.txt'))
            
            copied_original += 1
    
    # 2. Copiere date externe
    ext_images = os.path.join(external_dir, 'images')
    ext_labels = os.path.join(external_dir, 'labels')
    
    if os.path.exists(ext_images):
        for img_path in glob.glob(os.path.join(ext_images, '*.*')):
            h = file_hash(img_path)
            if h in seen_hashes:
                duplicates += 1
                continue
            seen_hashes.add(h)
            
            fname = os.path.basename(img_path)
            stem = os.path.splitext(fname)[0]
            
            shutil.copy2(img_path, os.path.join(output_dir, 'images', f'ext_{fname}'))
            label_path = os.path.join(ext_labels, f'{stem}.txt')
            if os.path.exists(label_path):
                shutil.copy2(label_path, os.path.join(output_dir, 'labels', f'ext_{stem}.txt'))
            
            copied_external += 1
    
    total = copied_original + copied_external
    original_ratio = copied_original / total if total > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"REZULTAT COMBINARE DATASETS")
    print(f"{'='*50}")
    print(f"Date proprii (Steinel): {copied_original} ({original_ratio*100:.1f}%)")
    print(f"Date externe:   {copied_external} ({(1-original_ratio)*100:.1f}%)")
    print(f"Duplicate eliminate: {duplicates}")
    print(f"Total: {total}")
    
    if original_ratio < min_original_ratio:
        print(f"\n⚠️ ATENȚIE: Procentul de date proprii ({original_ratio*100:.1f}%) "
              f"este sub minimul de {min_original_ratio*100:.0f}%!")
    else:
        print(f"\n✅ Procentul de date proprii respectă cerința de ≥{min_original_ratio*100:.0f}%")
    
    return total, copied_original, copied_external


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 4:
        combine_datasets(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Utilizare: python combine_datasets.py <generated_dir> <external_dir> <output_dir>")
