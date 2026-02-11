# Modul 1: Generare și Achiziție Date PCB

## Descriere

Acest modul conține scripturile pentru achiziția și gestionarea datelor
folosite în antrenarea modelului de detecție defecte PCB.

### Date proprii (~400 imagini)
Colectate în vara anului 2025 în cadrul unui internship la **Steinel Electronic**, Curtea de Argeș.
Imaginile au fost capturate direct de pe linia de producție, fotografiind PCB-uri reale
cu diverse tipuri de defecte, și adnotate manual în format YOLO.

## Scripturi

### generate.py
Script auxiliar pentru generarea de imagini sintetice suplimentare PCB cu defecte controlate.
Generează imagini cu adnotări în format YOLO (pentru completare dataset dacă este necesar).

### Utilități cameră
- `scan_cameras.py` – Scanare camere disponibile
- `debug_camera.py` – Debug cameră USB  
- `debug_droidcam.py` – Debug DroidCam
- `find_droidcam_url.py` – Găsire URL stream DroidCam
- `test_droidcam.py` – Test conectivitate DroidCam
- `test_all_cameras.py` – Test comprehensiv toate camerele
- `test_ai_detection.py` – Test inferență AI pe frame cameră
- `debug_serial.py` – Debug comunicare serială Arduino

## Date Proprii

Cele ~400 de imagini proprii sunt salvate în `data/generated/` (colectate la Steinel Electronic, vara 2025).
În antrenarea principală, acestea reprezintă ~3.6% din totalul de ~11.000 imagini – s-a optat pentru
această proporție în favoarea calității antrenării (un dataset extern mare și variat produce metrici mai bune). În cadrul
internship-ului, s-a realizat și o antrenare pe ~1000 de imagini (~40% date proprii).

## Utilizare

```bash
# Generare date sintetice
python generate.py --output ../../data/generated --count 500

# Scanare camere disponibile
python scan_cameras.py

# Test detecție AI
python test_ai_detection.py
```
