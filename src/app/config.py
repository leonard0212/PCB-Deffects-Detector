# config.py - Configurație aplicație AOI PCB Inspection
import os

# --- Căi proiect ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# --- Setări Serial ---
SERIAL_PORT = 'COM4'   # <--- VERIFICĂ în Device Manager!
BAUD_RATE = 9600

# --- Setări Cameră ---
CAMERA_INDEX = 2  # Index cameră (selectabil în GUI)

# --- Setări AI ---
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "pcb_model.pt")
CONFIDENCE_THRESHOLD = 0.45 # Cât de sigur să fie AI-ul (0-1)
IMG_SIZE = 640
