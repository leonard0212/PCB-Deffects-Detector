# debug_serial.py - Debug comunicare serială cu Arduino
import time
import serial
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from config import SERIAL_PORT, BAUD_RATE


def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"[DEBUG] Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
    try:
        while True:
            if ser.in_waiting:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    print(f"[ARDUINO] {line}")
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        print("[DEBUG] Closed")


if __name__ == "__main__":
    main()
