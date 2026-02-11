# Dataset – PCB Defect Detection

## Descriere

Dataset pentru detecția automată a defectelor pe plăci de circuite imprimate (PCB).

### Clase de Defecte (6)

| ID | Clasă | Descriere |
|----|-------|-----------|
| 0 | missing_hole | Lipsa găurii de montaj |
| 1 | mouse_bite | Deteriorare margine PCB |
| 2 | open_circuit | Circuit deschis (întrerupere pistă) |
| 3 | short | Scurtcircuit între piste |
| 4 | spur | Proeminență pe pistă |
| 5 | spurious_copper | Cupru rezidual nedorit |

## Structura Directoarelor

```
data/
├── raw/               # Date brute originale (nemodificate)
├── processed/         # Date curățate și transformate
├── generated/         # Date proprii (~400 imagini, internship Steinel Electronic 2025)
├── train/             # Set antrenare (70%)
│   ├── images/
│   └── labels/
├── validation/        # Set validare (15%)
│   ├── images/
│   └── labels/
└── test/              # Set testare (15%)
    ├── images/
    └── labels/
```

## Format Adnotări

Adnotările sunt în format **YOLO** (un fișier `.txt` per imagine):

```
<class_id> <x_center> <y_center> <width> <height>
```

Toate valorile sunt normalizate în intervalul [0, 1] relativ la dimensiunea imaginii.

## Surse Date

### Date Externe
- **PCB Defects Dataset** – disponibil pe Kaggle/Roboflow
- Imagini PCB reale cu adnotări manuale

### Date Proprii (~400 imagini, ~3.6% din dataset-ul principal de ~11.000)
- **Colectate în vara 2025** în cadrul unui internship la **Steinel Electronic**, Curtea de Argeș
- Fotografii reale de pe linia de producție cu defecte adnotate manual
- Acoperă toate cele 6 clase de defecte
- În cadrul internship-ului, s-a realizat și o antrenare pe ~1000 imagini (~40% date proprii)

## Împărțire Dataset

| Set | Procent | Utilizare |
|-----|---------|-----------|
| Train | 70% | Antrenare model |
| Validation | 15% | Tuning hiperparametri |
| Test | 15% | Evaluare finală |

## Reproducibilitate

Seed: 42 (vezi `src/preprocessing/data_splitter.py`)
