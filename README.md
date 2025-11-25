# Sistem de Inspecție Optică Automată (AOI) pentru PCB  
Detecție Defecte de Sudură cu Raspberry Pi 5 + YOLOv11

Acest proiect implementează un sistem de inspecție optică automată (AOI) pentru plăci electronice (PCB), utilizând Raspberry Pi 5 și algoritmi avansați de viziune computerizată (YOLOv11). Sistemul rulează autonom (edge computing), oferă feedback vizual în timp real și semnalizare hardware prin GPIO.

---

## 🔍 Funcționalități

Sistemul capturează imagini de înaltă calitate, le procesează cu o rețea neurală antrenată și identifică următoarele defecte:

- **Solder Bridge** – scurtcircuit între pini  
- **Cold Joint** – lipitură rece / granulată  
- **Missing Component** – componentă lipsă  
- **Excess Solder** – cositor în exces  

Rezultatele sunt afișate în două moduri:
- într-o **interfață web locală**,  
- printr-un **LED/releu** conectat la GPIO.

---

## 🧰 Cerințe Hardware

| Componentă | Detalii recomandate |
|-----------|----------------------|
| **Unitate procesare** | Raspberry Pi 5 (8 GB RAM recomandat), cu răcire activă |
| **Cameră** | Raspberry Pi HQ Camera / Arducam IMX477 |
| **Optică** | Lentilă macro cu distanță focală fixă |
| **Iluminare** | Ring light difuz pentru eliminarea reflexiilor |

---

## ⚙️ Instalare

### 1. Actualizare sistem
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install libatlas-base-dev python3-opencv -y
```

### 2. Configurare proiect
```bash
# Creare director proiect
mkdir aoi_system && cd aoi_system

# Creare și activare mediu virtual
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalare librării Python
```bash
pip install ultralytics opencv-python-headless flask RPi.GPIO
```

### 4. Integrare model AI
Plasați în directorul proiectului fișierul modelului YOLO antrenat (`best.pt` sau modelul exportat NCNN).

---

## ▶️ Utilizare

### Pornire sistem
```bash
python app_inspectie.py
```

### Accesare interfață web
Introduceți în browser, de pe un dispozitiv în aceeași rețea:
```
http://<IP_RASPBERRY_PI>:5000
```

Interfața afișează:
- fluxul video live,  
- bounding boxes peste defectele detectate,  
- starea curentă a plăcii (OK / DEFECT).

---

## 🔧 Configurare Parametri

Parametrii principali se modifică în `app_inspectie.py`:

| Variabilă | Descriere |
|-----------|-----------|
| `MODEL_PATH` | Calea către model (.pt / .onnx / ncnn) |
| `CAMERA_ID` | Indexul camerei (implicit 0) |
| `CONFIDENCE_THRESHOLD` | Prag detectare (0.0–1.0) |
| `IO_RELAY_PIN` | Pin BCM pentru semnalizarea externă |

---

## ⚡ Optimizare Performanță

Raspberry Pi nu rulează eficient modele `.pt`. Pentru 15–30 FPS, exportați modelul în format **NCNN**:

```python
from ultralytics import YOLO

model = YOLO('best.pt')
model.export(format='ncnn')
```

Copiați folderul NCNN pe Raspberry Pi și actualizați `MODEL_PATH`.

---

## 🛠️ Troubleshooting

### ❌ Eroare: `libGL.so.1` lipsește
```bash
sudo apt install libgl1-mesa-glx
```

### 🔥 Supraîncălzire
- utilizați răcire activă (ventilator),  
- fără ventilator apare **thermal throttling**, scăzând performanța.

### 📷 Imagine neclară
- ajustați manual focalizarea lentilei;  
- textul de pe PCB trebuie să fie perfect clar pentru detecții corecte.

---

## 📄 Licență
Acest proiect poate fi utilizat și modificat liber, conform licenței alese în repository.
