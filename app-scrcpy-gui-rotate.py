import tkinter as tk
import os
import subprocess
import time

class ScrcpyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrcpy Orientation Selector")
        self.root.geometry("300x150")

        # Path to scrcpy.exe
        self.scrcpy_path = r"C:\scrcpy-win64-v2.7\scrcpy.exe"
        
        # Variabel untuk menyimpan proses scrcpy yang sedang berjalan dan orientasi saat ini
        self.scrcpy_process = None
        self.current_orientation = None

        # Membuat tombol orientasi
        self.orientations = [
            "Potrait (0°)",
            "Landscape (90°)"
        ]
        self.create_buttons()

        # Menangani event saat jendela ditutup
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Mulai scrcpy saat aplikasi dimulai
        self.run_scrcpy()

    def create_buttons(self):
        """Membuat tombol-tombol orientasi pada GUI."""
        for orientation in self.orientations:
            btn = tk.Button(self.root, text=orientation, command=lambda o=orientation: self.change_orientation(o))
            btn.pack(fill="x", pady=5)

    def change_rotation(self, rotation_value):
        """Mengubah orientasi layar perangkat."""
        os.system(f"adb shell settings put system user_rotation {rotation_value}")
        time.sleep(1)  # Memberikan jeda waktu agar perubahan orientasi diterapkan

    def set_video_orientation(self, orientation):
        """Mengubah orientasi video di scrcpy tanpa menutup dan membuka kembali."""
        os.system(f"adb shell am broadcast -a com.genymobile.scrcpy.action.SET_LOCK_VIDEO_ORIENTATION --ei orientation {orientation}")

    def close_scrcpy(self):
        """Menutup proses scrcpy yang sedang berjalan."""
        if self.scrcpy_process is not None:
            self.scrcpy_process.terminate()
            self.scrcpy_process.wait()  # Menunggu proses scrcpy benar-benar tertutup
            self.scrcpy_process = None
            print("scrcpy closed")

    def run_scrcpy(self):
        """Menjalankan scrcpy."""
        if self.scrcpy_process is None:
            cmd = [self.scrcpy_path]
            self.scrcpy_process = subprocess.Popen(cmd)
            print("scrcpy started")

    def change_orientation(self, orientation):
        """Mengubah orientasi perangkat dan orientasi video di scrcpy."""
        orientations = {
            "Potrait (0°)": (0, 0),  # (user_rotation, video_orientation)
            "Landscape (90°)": (1, 1)  # (user_rotation, video_orientation)
        }

        # Hanya ubah jika orientasi baru berbeda dari yang saat ini
        if orientation != self.current_orientation:
            user_rotation, video_orientation = orientations[orientation]
            
            # Mengubah orientasi perangkat
            self.change_rotation(user_rotation)
            
            # Mengubah orientasi video di scrcpy tanpa restart
            self.set_video_orientation(video_orientation)
            
            self.current_orientation = orientation
            print(f"Orientation changed to {orientation}")

    def on_closing(self):
        """Menutup scrcpy dan GUI saat jendela ditutup."""
        self.close_scrcpy()
        self.root.destroy()  # Menutup GUI

# Membuat instance dari tkinter dan ScrcpyApp
if __name__ == "__main__":
    root = tk.Tk()
    app = ScrcpyApp(root)
    root.mainloop()
