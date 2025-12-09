# 📘 Proiect SIA – Sistem de Detecție Defecte PCB

**Disciplina:** Rețele Neuronale  
**Etapa:** 4 - Dezvoltarea Arhitecturii Aplicației Software  
**Student:** Popescu Leonard  
**Grupa:** 631AB  
**Data:** 09.12.2025

---

## Descriere

Sistem cu Inteligență Artificială (SIA) pentru detectarea defectelor de fabricație pe plăcile de circuite imprimate (PCB). Aplicația folosește o arhitectură modulară (OOP) și integrează un model YOLOv11 într-o interfață grafică (Tkinter).

Scopul etapei 4: livrarea unui schelet funcțional Pipeline: Date -> Model -> UI.

---

## Structura proiectului

```
Proiect_PCB_SIA/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── state_machine.png
│   └── screenshots/
├── models/
│   └── best.pt
├── src/
│   ├── data_acquisition/
│   │   └── loader.py
│   ├── neural_network/
│   │   └── yolo_wrapper.py
│   └── ui/
│       └── app_gui.py
├── main.py
└── README.md
```

---

## Arhitectura și fluxul aplicației

Aplicația are 3 module principale în `src/`:

- data_acquisition: descărcare/gestionare dataset (Roboflow).
- neural_network: wrapper pentru modelul YOLO (fișier `yolo_wrapper.py`).
- ui: interfața grafică (Tkinter) cu încărcare imagine, slider pentru confidence, buton detectare și vizualizare rezultate.

Stări principale (rezumat):
- Initialization: verifică folderele și modelul `models/best.pt`.
- Idle: așteaptă input utilizator.
- Image Loading: încărcare și validare imagine.
- AI Processing: conversie -> predict (clasa PCBModel).
- Result Visualization: desenare bounding boxes și afișare.
- Error Handling: pop-up la excepții.

Diagrama completă: `docs/state_machine.png`.

---

## Detalii tehnice pe module

- Modul 1 — Data Acquisition (`src/data_acquisition`): DatasetLoader (Roboflow), format YOLO (imagini + .txt).
- Modul 2 — Neural Network (`src/neural_network`): YOLOv11n (wrapper `PCBModel`), optimizat pentru CPU.
- Modul 3 — UI (`src/ui`): Tkinter, slider pentru prag de încredere, afișare imagine și status.

---

## Cerințe și instalare (Windows)

- OS: Windows 10/11  
- Python: 3.11 (recomandat pentru compatibilitate PyTorch/Ultralytics)

1. Deschide PowerShell sau CMD în folderul proiectului:
```powershell
py -3.11 -m pip install --upgrade pip
py -3.11 -m pip install ultralytics pillow opencv-python roboflow
```

2. Plasează modelul antrenat:
- Copiază `best.pt` în `Proiect_PCB_SIA/models/best.pt`.

3. Rulează aplicația:
```powershell
py -3.11 main.py
```

---

## Observații

- Dataset raw poate să nu fie prezent (antrenare făcută în Google Colab).
- Ajustați pragul de încredere din UI pentru a regla sensibilitatea detectării.
- Logica modelului este încapsulată în `yolo_wrapper.py` pentru a permite înlocuirea ulterioară fără modificări majore în UI.

---

## Contact / Autor
Popescu Leonard — Grupa 631AB

---
