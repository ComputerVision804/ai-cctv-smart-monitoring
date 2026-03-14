import tkinter as tk
import tkinter.messagebox as messagebox
import cv2
import time

def show_alert(count):

    root = tk.Tk()
    root.withdraw()

    messagebox.showwarning(
        "Suspicious Activity",
        f"Too many people detected: {count}"
    )

    root.destroy()

def save_alert(frame):

    filename = f"static/screenshots/alert_{int(time.time())}.jpg"
    cv2.imwrite(filename, frame)

    return filename