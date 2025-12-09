import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from src.neural_network.yolo_wrapper import PCBModel

class PCBDetectorApp:
    def __init__(self, root, model_path):
        self.root = root
        self.root.title("PCB Defect Detector - SIA Etapa 4")
        self.root.geometry("1100x700")
        
        self.ai_engine = PCBModel(model_path)
        self.current_image = None
        self.setup_ui()

    def setup_ui(self):
        # Panou Stânga
        control = tk.Frame(self.root, bg="#f4f4f4", width=250)
        control.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(control, text="Panou Control", font=("Arial", 14, "bold"), bg="#f4f4f4").pack(pady=20)
        
        tk.Button(control, text="📂 1. Încarcă Imagine", bg="#007acc", fg="white", 
                  font=("Arial", 10), command=self.load_image).pack(fill=tk.X, padx=20, pady=10)

        self.conf_lbl = tk.Label(control, text="Sensibilitate: 0.40", bg="#f4f4f4")
        self.conf_lbl.pack(pady=(20,0))
        
        self.slider = tk.Scale(control, from_=0.1, to=1.0, resolution=0.05, orient=tk.HORIZONTAL,
                               command=lambda v: self.conf_lbl.config(text=f"Sensibilitate: {v}"))
        self.slider.set(0.40)
        self.slider.pack(fill=tk.X, padx=20)

        tk.Button(control, text="🔍 2. Analizează", bg="#28a745", fg="white", 
                  font=("Arial", 11, "bold"), command=self.process).pack(fill=tk.X, padx=20, pady=20)
        
        self.status = tk.Label(control, text="Status: Așteptare", bg="#ddd", height=3)
        self.status.pack(fill=tk.X, padx=20, pady=20)

        # Panou Dreapta
        self.canvas = tk.Label(self.root, text="Nicio imagine", bg="#ccc")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Imagini", "*.jpg *.png *.bmp")])
        if path:
            self.current_image = Image.open(path)
            self._show(self.current_image)
            self.status.config(text="Imagine încărcată.", bg="#add8e6")

    def process(self):
        if not self.current_image: return
        if not self.ai_engine.model:
            messagebox.showerror("Eroare", "Modelul nu este încărcat!")
            return
            
        res = self.ai_engine.predict(np.array(self.current_image), confidence=self.slider.get())
        if res:
            res_plotted = res.plot()
            img_res = Image.fromarray(cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB))
            self._show(img_res)
            self.status.config(text=f"Defecte: {len(res.boxes)}", bg="#90ee90")

    def _show(self, img):
        # Resize simplu pentru display
        base_h = 600
        w, h = img.size
        ratio = (base_h / float(h))
        w_new = int((float(w) * float(ratio)))
        img = img.resize((w_new, base_h), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        self.canvas.config(image=tk_img, text="")
        self.canvas.image = tk_img
