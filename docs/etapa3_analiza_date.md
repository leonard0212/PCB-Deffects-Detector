# Etapa 3 – Analiza Datelor

> **Student:** Leonard Popescu • FIIR–SIA–II, 631AB

## 3.1 Descriere Dataset

Proiectul utilizează un dataset de imagini PCB (Printed Circuit Board) cu defecte adnotate
pentru antrenarea unui model de detecție de obiecte YOLOv11.

### Sursa Datelor
- **Date externe**: Dataset PCB Defects disponibil pe platforme publice (Kaggle, Roboflow)
- **Date proprii (~400 imagini)**: Colectate în vara anului 2025 în cadrul unui internship la **Steinel Electronic**, Curtea de Argeș. Imaginile au fost capturate direct de pe linia de producție, fotografiind PCB-uri reale cu diverse tipuri de defecte și adnotate manual în format YOLO.

### Dimensiuni Dataset
- **Format imagine**: JPEG/PNG, 640×640 pixeli
- **Format adnotări**: YOLO (text, per imagine)
- **Clase**: 6 tipuri de defecte PCB

## 3.2 Clasele de Defecte

| ID | Clasă | Descriere | Frecvență |
|----|-------|-----------|-----------|
| 0 | missing_hole | Lipsa găurii de montaj | ~16.7% |
| 1 | mouse_bite | Deteriorare margine PCB | ~16.7% |
| 2 | open_circuit | Circuit deschis | ~16.7% |
| 3 | short | Scurtcircuit între piste | ~16.7% |
| 4 | spur | Proeminență pe pistă | ~16.7% |
| 5 | spurious_copper | Cupru rezidual | ~16.7% |

Dataset-ul este relativ echilibrat între clase.

## 3.3 Analiza Exploratorie

### Statistici Imagini
- **Rezoluție**: Imagini originale de diverse dimensiuni, redimensionate la 640×640 pentru antrenare
- **Canale**: 3 (RGB/BGR)
- **Luminozitate medie**: variabilă (PCB-uri verzi/maronii/albastre)

### Calitatea Datelor
- Imagini verificate prin `src/preprocessing/data_cleaner.py`
- Adnotări validate (format YOLO, coordonate [0,1])
- Imagini corupte sau prea mici eliminate automat

## 3.4 Preprocesare Aplicată

1. **Curățare**: Eliminare imagini corupte, verificare adnotări
2. **Redimensionare**: 640×640 pixeli (standard YOLO)
3. **Normalizare**: Pixeli scalati [0, 255] → [0, 1] intern de YOLO
4. **Split**: 70% train / 15% validation / 15% test (seed=42)

## 3.5 Augmentări (în antrenare)

| Augmentare | Parametru | Valoare |
|------------|-----------|---------|
| HSV Hue | hsv_h | 0.015 |
| HSV Saturation | hsv_s | 0.7 |
| HSV Value | hsv_v | 0.4 |
| Horizontal Flip | fliplr | 0.5 |
| Mosaic | mosaic | 1.0 |
| Scale | scale | 0.5 |
| Translation | translate | 0.1 |
| Erasing | erasing | 0.4 |

## 3.6 Contribuția Datelor Proprii

Dataset-ul de date proprii conține **~400 de imagini** colectate pe parcursul verii 2025 în cadrul unui internship la **Steinel Electronic**, Curtea de Argeș. Imaginile au fost capturate direct din mediul industrial, de pe linia de inspecție a fabricii, acoperind toate cele 6 clase de defecte.

În antrenarea principală (modelul `pcb_model.pt`), datele proprii reprezintă **~3.6%** din totalul dataset-ului (400 din ~11.000 imagini). Decizia de a nu forța un prag de 40% a fost luată deliberat: am prioritizat calitatea antrenării, iar un dataset extern mare și variat a condus la metrici semnificativ mai bune (mAP@50 = 98.6%) față de varianta cu proporție forțată.

În cadrul internship-ului de la Steinel Electronic, am efectuat și o antrenare pe un subset mai mic de **~1000 de imagini** (incluzând cele 400 proprii, deci ~40% date proprii), obținând un model funcțional dar cu metrici ușor inferioare. Modelul `.pt` corespunzător acestei antrenări este disponibil în `models/`.

Combinarea datelor se face prin `src/preprocessing/combine_datasets.py`.
