<!-- filepath: c:\Users\leonard.popescu\OneDrive - GRADINARIU IMPORT EXPORT SRL\Desktop\Proiect_PCB_SIA\README_Etapa4_Arhitectura_SIA_03.12.2025.md -->
# 📘 Proiect SIA – Sistem de Detecție Defecte PCB

**Disciplina:** Rețele Neuronale  
**Etapa:** 4 - Dezvoltarea Arhitecturii Aplicației Software  
**Student:** Popescu Leonard  
**Grupa:** 631AB  
**Data:** 09.12.2025

---

## 1. Descrierea Proiectului

Acest proiect implementează un **Sistem cu Inteligență Artificială (SIA)** capabil să detecteze automat defectele de fabricație pe plăcile de circuite imprimate (PCB). Aplicația utilizează o arhitectură modulară, bazată pe **Programare Orientată pe Obiecte (OOP)**, integrând un model de Deep Learning (**YOLOv11**) într-o interfață grafică prietenoasă.

**Scopul etapei curente (Etapa 4):** Livrarea unui schelet funcțional complet (Pipeline: *Date -> Model -> UI*) care să demonstreze arhitectura sistemului.

---

## 2. Arhitectura Sistemului

Proiectul este structurat pe 3 module principale, situate în folderul `src/`. Structura completă a repository-ului este următoarea:

```text
Proiect_PCB_SIA/
├── data/                  # Stocarea datelor
│   ├── raw/               # Imagini descărcate de pe Roboflow (nu exista pentru ca am antrenat modelul in Google Colab)
│   └── processed/         # Imagini preprocesate (dacă e cazul)
├── docs/                  # Documentație și Diagrame
│   ├── state_machine.png  # Diagrama stărilor aplicației
│   └── screenshots/       # Capturi de ecran
├── models/                # Modelele antrenate (.pt)
│   └── best.pt            # Modelul YOLO curent
├── src/                   # Codul Sursă Modular
│   ├── data_acquisition/  # Modul 1: Achiziție Date
│   │   └── loader.py      # Script descărcare Roboflow
│   ├── neural_network/    # Modul 2: Rețea Neuronală
│   │   └── yolo_wrapper.py# Clasa Wrapper peste Ultralytics
│   └── ui/                # Modul 3: Interfață Grafică
│       └── app_gui.py     # Logica ferestrei Tkinter
├── main.py                # Punctul de intrare (Entry Point)
└── README.md              # Acest fișier
```

---

## 3. Diagrama de Stări (State Machine)

Diagrama UML de stări se găsește în `docs/state_machine.png`. Mai jos este legenda detaliată a tranzițiilor logice ale aplicației:

### 🔹 Initialization (Inițializare)
* **Declanșare:** La pornirea `main.py`.
* **Acțiune:** Sistemul verifică existența folderelor critice și a modelului `models/best.pt`. Se instanțiază clasa `PCBDetectorApp` și se încarcă biblioteca YOLO.

### 🔹 Idle (Așteptare)
* **Descriere:** Starea de repaus. Aplicația așteaptă o acțiune a utilizatorului.
* **Resurse:** Consumul de resurse este minim.

### 🔹 Image Loading (Încărcare_Imagine)
* **Tranziție:** Utilizatorul apasă butonul **"Încarcă Imagine"**.
* **Acțiune:**
    1. Se deschide un dialog nativ de fișiere.
    2. Imaginea selectată este validată.
    3. Imaginea este redimensionată (*resize cu păstrarea aspect ratio*) pentru a fi afișată în GUI.
* **Ieșire:** Revine în starea *Idle* cu imaginea încărcată în memorie.

### 🔹 AI Processing (Procesare_AI)
* **Tranziție:** Utilizatorul apasă butonul **"Detectează"**.
* **Acțiune:**
    1. Imaginea este convertită din format `PIL` în format `Numpy array`.
    2. Clasa `PCBModel` preia array-ul și rulează inferența (metoda `predict`).
* **Parametri:** Se folosește pragul de confidență setat din slider-ul interfeței.

### 🔹 Result Visualization (Vizualizare_Rezultate)
* **Acțiune:**
    1. Rezultatele inferenței (coordonate bounding boxes) sunt desenate peste imaginea originală.
    2. Imaginea rezultată este convertită înapoi în format compatibil `Tkinter` și afișată utilizatorului.
    3. Statusul se actualizează cu numărul de defecte găsite.

### 🔹 Error Handling (Gestionare_Erori)
* **Acțiune:** Orice excepție (fișier lipsă, format incompatibil) declanșează un pop-up de eroare, protejând aplicația de crash.

---

## 4. Detalii Tehnice Module

### 📦 Modul 1: Data Acquisition
* **Locație:** `src/data_acquisition`
* **Sursă Date:** Roboflow (Dataset PCB Defect).
* **Funcționalitate:** Clasa `DatasetLoader` permite descărcarea automată și versionată a setului de date folosind un API Key.
* **Format:** Imaginile sunt descărcate în format compatibil YOLOv11 (imagini + fișiere `.txt` pentru etichete).

### 🧠 Modul 2: Neural Network
* **Locație:** `src/neural_network`
* **Model:** YOLOv11n (Nano) - optimizat pentru viteză pe CPU.
* **Implementare OOP:** Clasa `PCBModel` (în fișierul `yolo_wrapper.py`) încapsulează logica bibliotecii Ultralytics.
* **Justificare:** Folosirea unui wrapper (înveliș) permite înlocuirea ușoară a modelului YOLO cu o altă arhitectură în viitor, fără a fi necesară modificarea restului aplicației.

### 🖥️ Modul 3: User Interface
* **Locație:** `src/ui`
* **Tehnologie:** `Tkinter` (Standard Python GUI).
* **Features:**
    * Vizualizare imagine în timp real.
    * Slider pentru ajustarea sensibilității (*Confidence Threshold*) în mod dinamic.
    * Feedback vizual rapid prin etichete de status colorate.

## 5. Instrucțiuni de Instalare și Rulare

### ⚙️ Cerințe de Sistem
* **OS:** Windows 10/11
* **Limbaj:** Python 3.11 (Obligatoriu pentru compatibilitate PyTorch)

### Pasul 1: Instalare Dependențe
Deschideți terminalul (PowerShell sau CMD) în folderul proiectului și rulați comanda:

```bash
py -3.11 -m pip install ultralytics pillow opencv-python roboflow
```

### Pasul 2: Plasare Model
Asigurați-vă că fișierul modelului antrenat (`best.pt`) este copiat în folderul corect, astfel încât calea să fie:

`Proiect_PCB_SIA/models/best.pt`

### Pasul 3: Rulare Aplicație
Pentru a porni interfața grafică, rulați comanda:

```bash
py -3.11 main.py
```
