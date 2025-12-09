import os
import sys
import tkinter as tk
from src.ui.app_gui import PCBDetectorApp

# Calea către model
MODEL_PATH = os.path.join("models", "best.pt")

def main():
    if not os.path.exists("models"):
        os.makedirs("models")
    
    # Verificare existență model
    final_model_path = MODEL_PATH
    if not os.path.exists(MODEL_PATH):
        # Fallback: verificăm dacă e în root
        if os.path.exists("best.pt"):
            final_model_path = "best.pt"
            print("[Info] Model găsit în root, nu în folderul models.")
        else:
            print("[Atenție] Fișierul 'best.pt' lipsește! Copiază-l în folderul 'models'.")

    root = tk.Tk()
    app = PCBDetectorApp(root, model_path=final_model_path)
    root.mainloop()

if __name__ == "__main__":
    main()
