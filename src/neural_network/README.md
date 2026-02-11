# Modul 2: Rețea Neuronală – Detecție Defecte PCB

## Arhitectură

Modelul folosit este **YOLOv11n** (nano), optimizat pentru detecția de obiecte în timp real.

### Specificații Model
- **Bază**: YOLOv11n pretrained pe COCO
- **Task**: Object Detection (`detect`)
- **Input**: Imagini 640×640 px (RGB)
- **Output**: Bounding boxes + clase defecte + confidence scores
- **Clase detectate**: 6 tipuri de defecte PCB (missing_hole, mouse_bite, open_circuit, short, spur, spurious_copper)

### Hiperparametri Principali
| Parametru | Valoare |
|-----------|---------|
| Epoci | 100 (early stopping la 52) |
| Batch size | 16 |
| Image size | 640 |
| Optimizer | auto (AdamW) |
| LR inițial | 0.01 |
| LR final | 0.01 |
| Momentum | 0.937 |
| Weight decay | 0.0005 |
| Patience | 25 |

### Augmentări
- HSV Hue: 0.015, Saturation: 0.7, Value: 0.4
- Flip LR: 0.5
- Mosaic: 1.0
- Scale: 0.5
- Translate: 0.1
- Erasing: 0.4

## Metrici Finale (Epoca 52 – Best)
| Metrică | Valoare |
|---------|---------|
| Precision | 0.9765 |
| Recall | 0.9812 |
| mAP@50 | 0.9859 |
| mAP@50-95 | 0.5629 |
| Val Box Loss | 1.5245 |
| Val Cls Loss | 0.6151 |

## Scripturi

| Script | Descriere |
|--------|-----------|
| `model.py` | Definirea arhitecturii modelului YOLOv11 |
| `train.py` | Antrenare model pe dataset PCB |
| `evaluate.py` | Evaluare metrici pe test set |
| `optimize.py` | Experimente optimizare hiperparametri |
| `visualize.py` | Generare grafice (loss curves, metrici, confusion matrix) |
