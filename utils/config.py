# utils/config.py
import os
import json

def load_config():
    """Muat konfigurasi dari file konfigurasi"""
    config_path = 'config.json'
    
    # Buat config default jika tidak ada
    default_config = {
        'backend_url': 'http://127.0.0.1:5000',
        'download_folder': os.path.join(os.path.expanduser('~'), 'Downloads', 'YouTube Downloader')
    }
    
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    
    # Baca konfigurasi yang ada
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Ensure download folder exists
        if not os.path.exists(config['download_folder']):
            os.makedirs(config['download_folder'], exist_ok=True)
            
        return config
    except:
        return default_config