# main.py - Aplicație principală AOI PCB Inspection System
# Autor: Leonard Popescu | FIIR–SIA–II, 631AB
import sys
import os

# Adaugă directorul rădăcină al proiectului în PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src', 'app'))

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import time
import winsound

from config import SERIAL_PORT, BAUD_RATE, CAMERA_INDEX, MODEL_PATH, CONFIDENCE_THRESHOLD
from serial_comm import SerialManager
from camera import CameraManager
from ai_inference import AIModel

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AOI PCB Inspection System - NextLab")
        self.root.geometry("1000x700")
        
        # 1. Inițializare Module
        self.serial = SerialManager(SERIAL_PORT, BAUD_RATE)
        self.cam = CameraManager(CAMERA_INDEX)
        self.ai = AIModel(MODEL_PATH, CONFIDENCE_THRESHOLD)
        
        self.inspecting = False # Dacă AI-ul scanează activ
        self.conveyor_active = False
        self.scan_pending = False
        self.scan_ready_time = 0.0
        self.last_scan_frame = None
        self.alarm_active = False
        self.alarm_next_beep = 0.0
        self.last_arduino_log_time = 0.0
        self.last_scan_time = 0.0
        self.last_pcb_seen_time = 0.0

        # 2. Interfața Grafică (GUI)
        self.setup_gui()

        # 3. Conectare Serială Automată
        if self.serial.connect():
            self.lbl_status.config(text="Status: CONECTAT", fg="green")
        else:
            self.lbl_status.config(text="Status: FĂRĂ SERIAL (continuare fără Arduino)", fg="orange")
            self.log("⚠️ Arduino nu e conectat - programul continuă fără control bandă")

        # 4. Loop Video
        self.video_loop()

    def setup_gui(self):
        # Frame Stânga (Video)
        self.frame_video = tk.Frame(self.root, bg="black", width=640, height=480)
        self.frame_video.pack(side=tk.LEFT, padx=10, pady=10)
        self.lbl_video = tk.Label(self.frame_video)
        self.lbl_video.pack()

        # Frame Dreapta (Controale)
        self.frame_ctrl = tk.Frame(self.root)
        self.frame_ctrl.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(self.frame_ctrl, text="Panou Control", font=("Arial", 16, "bold")).pack(pady=20)

        # Selector Cameră
        tk.Label(self.frame_ctrl, text="Index Cameră:", font=("Arial", 10)).pack(pady=(10, 0))
        self.camera_var = tk.StringVar(value=str(CAMERA_INDEX))
        camera_frame = tk.Frame(self.frame_ctrl)
        camera_frame.pack(pady=5)
        for i in range(4):
            tk.Radiobutton(camera_frame, text=str(i), variable=self.camera_var, value=str(i), 
                          command=self.change_camera).pack(side=tk.LEFT, padx=5)

        # Butoane
        btn_start = tk.Button(self.frame_ctrl, text="START BANDĂ", command=self.start_conveyor, 
                              bg="#2ecc71", fg="white", font=("Arial", 12), height=2, width=20)
        btn_start.pack(pady=5)

        btn_stop = tk.Button(self.frame_ctrl, text="STOP", command=self.stop_conveyor, 
                             bg="#e74c3c", fg="white", font=("Arial", 12), height=2, width=20)
        btn_stop.pack(pady=5)

        btn_reset = tk.Button(self.frame_ctrl, text="RESETARE ALARMĂ", command=self.reset_alarm, 
                              bg="#f39c12", fg="white", font=("Arial", 12), height=2, width=20)
        btn_reset.pack(pady=5)

        btn_scan = tk.Button(self.frame_ctrl, text="SCANARE ACUM", command=self.manual_scan, 
                            bg="#3498db", fg="white", font=("Arial", 12), height=2, width=20)
        btn_scan.pack(pady=5)

        # Indicator Status Inspecție
        self.lbl_inspection = tk.Label(self.frame_ctrl, text="Așteptare scanare...", 
                                       font=("Arial", 11, "bold"), bg="gray", fg="white", 
                                       padx=10, pady=10, relief=tk.RAISED)
        self.lbl_inspection.pack(pady=10, fill=tk.X)

        # Log Defecte
        tk.Label(self.frame_ctrl, text="Jurnal Inspecție:", font=("Arial", 12)).pack(pady=(20, 5))
        self.log_box = tk.Text(self.frame_ctrl, height=12, width=35)
        self.log_box.pack()

        # Status Bar
        self.lbl_status = tk.Label(self.root, text="Inițializare...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def start_conveyor(self):
        if self.alarm_active:
            self.log("ALARMĂ activă: resetare necesară înainte de pornire.")
            return
        self.serial.send_command('S')
        self.conveyor_active = True
        self.log("Comandă: Start Bandă")

    def stop_conveyor(self):
        self.serial.send_command('O')
        self.conveyor_active = False
        self.log("Comandă: Stop Bandă")

    def reset_alarm(self):
        print(f"[DEBUG] reset_alarm called, alarm_active={self.alarm_active}")
        if self.alarm_active:
            self.alarm_active = False
            self.last_scan_frame = None
            self.scan_pending = False  # Oprește orice scanare pendinte
            self.lbl_status.config(text="Status: RESETAT", fg="blue")
            self.lbl_inspection.config(text="Alarmă resetată. Gata de scanare.", bg="gray")
            self.log("✅ Alarmă resetată manual. Repornesc scanarea.")
            # Permite scanare imediată la următorul PCB
            self.last_scan_time = 0.0
        else:
            self.log("Nu există alarmă activă.")

    def manual_scan(self):
        print(f"[DEBUG] manual_scan called, alarm_active={self.alarm_active}")
        # Resetează alarma dacă e activă
        if self.alarm_active:
            self.alarm_active = False
            self.last_scan_frame = None
            self.log("📸 Resetare alarmă și scanare nouă...")
        else:
            self.log("📸 Scanare manuală inițiată...")
        
        self.scan_pending = True
        self.scan_ready_time = time.monotonic()
        print(f"[DEBUG] Scanare manuală setată - scan_pending={self.scan_pending}")

    def change_camera(self):
        cam_idx = int(self.camera_var.get())
        if cam_idx != self.cam.current_index:
            self.log(f"Schimbare cameră: {cam_idx}")
            self.cam.release()
            self.cam = CameraManager(cam_idx)
            if not self.cam.cap.isOpened():
                self.log(f"Eroare: Camera {cam_idx} nu e disponibilă!")
                self.camera_var.set(str(self.cam.current_index))
            else:
                self.log(f"OK: Camera {cam_idx} activă")

    def update_alarm(self, now):
        if self.alarm_active and now >= self.alarm_next_beep:
            try:
                winsound.Beep(1500, 150)
            except Exception:
                pass
            self.alarm_next_beep = now + 0.5

    def log(self, msg):
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)

    def is_pcb_present(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        edge_ratio = edges.mean() / 255.0
        return edge_ratio > 0.02

    def video_loop(self):
        now = time.monotonic()
        self.update_alarm(now)

        # 1. Citire Cadru Cameră
        frame, ret = self.cam.get_frame()
        if ret:
            display_frame = frame.copy()

            # Detectare PCB în cadru (fără senzor ultrasonic)
            pcb_present = self.is_pcb_present(frame)
            if pcb_present:
                self.last_pcb_seen_time = now

            # Dacă PCB e prezent, inițiază scanare periodică
            if pcb_present and not self.alarm_active and not self.scan_pending:
                if now - self.last_scan_time > 1.0:
                    self.scan_pending = True
                    self.scan_ready_time = now
                    self.last_scan_time = now
                    self.log("📸 PCB detectat în cadru. Scanare inițiată...")

            # Execută scanare dacă e programată
            if self.scan_pending and now >= self.scan_ready_time:
                self.log("🔍 Scanare în curs...")
                annotated_frame, defect_found, detections = self.ai.predict(frame)
                self.scan_pending = False
                self.last_scan_frame = annotated_frame.copy()

                if defect_found:
                    self.alarm_active = True
                    self.conveyor_active = False
                    self.serial.send_command('O')
                    self.lbl_status.config(text="Status: ALARMĂ DEFECT", fg="red")
                    det_text = ", ".join(detections) if detections else "necunoscut"
                    self.log(f"🔴 DEFECT DETECTAT: {det_text}")
                    self.lbl_inspection.config(text=f"⚠️ DEFECT: {det_text}", bg="red", fg="white")
                    display_frame = annotated_frame.copy()
                else:
                    self.alarm_active = False
                    self.log("✅ OK: fără defecte.")
                    self.lbl_status.config(text="Status: OK", fg="green")
                    self.lbl_inspection.config(text="✅ PCB OK - Fără defecte", bg="green", fg="white")
                    self.serial.send_command('S')
                    self.conveyor_active = True
                    display_frame = annotated_frame.copy()
            elif self.alarm_active and self.last_scan_frame is not None:
                # Afișează ultimul frame cu defecte detectate
                display_frame = self.last_scan_frame.copy()

            # Adaugă overlay text pe imagine pentru feedback vizual instant
            if self.alarm_active and self.last_scan_frame is not None:
                cv2.putText(display_frame, "DEFECT DETECTAT!", (10, 40), 
                           cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 3)
                cv2.rectangle(display_frame, (5, 5), (635, 475), (0, 0, 255), 3)
            else:
                # Feedback PCB prezent
                if (now - self.last_pcb_seen_time) < 0.5:
                    cv2.putText(display_frame, "PCB detectat", (10, 40),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            # 4. Conversie pentru Tkinter
            img = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lbl_video.imgtk = imgtk
            self.lbl_video.configure(image=imgtk)

        self.root.after(30, self.video_loop) # ~30 FPS

    def on_close(self):
        self.stop_conveyor()
        self.serial.close()
        self.cam.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
