# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.config import load_config

def main():
    # Memastikan aplikasi berjalan di direktori yang benar
    if getattr(sys, 'frozen', False):
        # Jika dijalankan sebagai executable
        application_path = os.path.dirname(sys.executable)
    else:
        # Jika dijalankan sebagai script
        application_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(application_path)
    
    # Pastikan direktori resources ada
    if not os.path.exists('resources'):
        os.makedirs('resources')
    
    # Cek apakah file tema ada, jika tidak buat
    if not os.path.exists("resources/dark_theme.qss"):
        with open("resources/dark_theme.qss", "w") as f:
            f.write("""/* QSS Theme file content here */""")
    
    # Load konfigurasi
    config = load_config()
    
    # Inisialisasi aplikasi
    app = QApplication(sys.argv)
    
    # Setel style sheet untuk tema gelap
    try:
        with open("resources/dark_theme.qss", "r") as f:
            app.setStyleSheet(f.read())
    except:
        print("Warning: Could not load stylesheet")
    
    # Buat dan tampilkan jendela utama
    window = MainWindow(config)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()