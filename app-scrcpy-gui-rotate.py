import tkinter as tk
import os
import subprocess
import time

# Path to scrcpy.exe
SCRCPY_PATH = r"C:\scrcpy-win64-v2.7\scrcpy.exe"

# Simpan PID process scrcpy yang sedang berjalan
scrcpy_process = None
current_orientation = None

def change_rotation(rotation_value):
    """Mengubah orientasi layar perangkat."""
    os.system(f"adb shell settings put system user_rotation {rotation_value}")
    time.sleep(1)  # Memberikan jeda waktu agar perubahan orientasi diterapkan

def set_video_orientation(orientation):
    """Mengubah orientasi video di scrcpy tanpa menutup dan membuka kembali."""
    os.system(f"adb shell am broadcast -a com.genymobile.scrcpy.action.SET_LOCK_VIDEO_ORIENTATION --ei orientation {orientation}")

def close_scrcpy():
    """Menutup proses scrcpy yang sedang berjalan."""
    global scrcpy_process
    if scrcpy_process is not None:
        scrcpy_process.terminate()
        scrcpy_process.wait()  # Menunggu proses scrcpy benar-benar tertutup
        scrcpy_process = None
        print("scrcpy closed")

def run_scrcpy():
    """Menjalankan scrcpy."""
    global scrcpy_process
    cmd = [SCRCPY_PATH]
    scrcpy_process = subprocess.Popen(cmd)
    print("scrcpy started")

def change_orientation(orientation):
    """Mengubah orientasi perangkat dan orientasi video di scrcpy."""
    global current_orientation
    orientations = {
        "Potrait (0°)": (0, 0),  # (user_rotation, video_orientation)
        "Landscape (90°)": (1, 1)  # (user_rotation, video_orientation)
    }

    # Hanya ubah jika orientasi baru berbeda dari yang saat ini
    if orientation != current_orientation:
        user_rotation, video_orientation = orientations[orientation]
        
        # Mengubah orientasi perangkat
        change_rotation(user_rotation)
        
        # Mengubah orientasi video di scrcpy tanpa restart
        set_video_orientation(video_orientation)
        
        current_orientation = orientation
        print(f"Orientation changed to {orientation}")

def on_closing():
    """Menutup scrcpy dan GUI saat jendela ditutup."""
    close_scrcpy()
    app.destroy()  # Menutup GUI

# Membuat GUI
app = tk.Tk()
app.title("Scrcpy Orientation Selector")

# Mulai scrcpy saat aplikasi dimulai
run_scrcpy()

# Buat tombol untuk setiap orientasi
orientations = [
    "Potrait (0°)",
    "Landscape (90°)"
]

for orientation in orientations:
    btn = tk.Button(app, text=orientation, command=lambda o=orientation: change_orientation(o))
    btn.pack(fill="x", pady=5)

# Menangani event saat jendela ditutup
app.protocol("WM_DELETE_WINDOW", on_closing)

app.geometry("300x150")
app.mainloop()
