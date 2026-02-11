# Modul 3: Aplicație AOI PCB Inspection

## Descriere

Acest modul conține aplicația principală a sistemului AOI (Automated Optical Inspection) pentru inspecția PCB-urilor. Aplicația integrează toate celelalte module (achiziție date, rețea neuronală, comunicare serială) într-o interfață grafică unificată.

## Arhitectură

Aplicația este construită cu **Tkinter** și oferă:
- **Feed video în timp real** de la cameră (USB / DroidCam)
- **Detecție automată PCB** în cadrul video (analiza edge-urilor)
- **Inferență AI** folosind modelul YOLOv11 antrenat pe defecte PCB
- **Control bandă transportoare** prin comunicare serială cu Arduino
- **Sistem de alarmă** cu feedback vizual și sonor la detectarea defectelor

## Lansare

```bash
cd src/app
python main.py
```

## Cerințe
- Python 3.9+
- Toate dependențele din `requirements.txt`
- (Opțional) Arduino conectat pe portul serial pentru control bandă
- Cameră USB sau DroidCam

## Configurare

Parametrii aplicației se configurează în `config.py`:
- `SERIAL_PORT` – portul COM al Arduino-ului
- `CAMERA_INDEX` – indexul camerei (selectabil și din GUI)
- `MODEL_PATH` – calea către modelul `.pt`
- `CONFIDENCE_THRESHOLD` – pragul de încredere AI (0–1)

## Fluxul Aplicației

1. **Pornire** → Conectare serială automată + inițializare cameră
2. **Loop video** → Captură cadru → Detectare PCB → Scanare AI periodică
3. **Defect detectat** → Oprire bandă + alarmă sonoră + afișare detecții
4. **Resetare alarmă** → Reluare scanare
