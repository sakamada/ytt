# utils/file_manager.py
import os
import glob

def list_downloaded_videos():
    """Dapatkan daftar video yang sudah didownload"""
    videos = []
    
    # Baca konfigurasi untuk mendapatkan folder download
    from utils.config import load_config
    config = load_config()
    download_folder = config['download_folder']
    
    # Cek folder backend juga jika ada
    backend_download_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'backend', 'downloads')
    
    # Daftar semua folder yang perlu dicek
    folders_to_check = [
        download_folder,
        backend_download_folder,
        'downloads',  # Relatif ke aplikasi
        os.path.join(os.path.expanduser('~'), 'Downloads')  # Downloads user
    ]
    
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
    
    for folder in folders_to_check:
        if os.path.exists(folder):
            for ext in video_extensions:
                pattern = os.path.join(folder, f'*{ext}')
                videos.extend(glob.glob(pattern))
    
    # Hapus duplikasi
    videos = list(set(videos))
    
    return videos
def get_video_thumbnail(video_path):
    """
    Membuat thumbnail untuk video
    Catatan: Fungsi ini memerlukan modul opencv-python untuk bekerja
    """
    try:
        import cv2
        import os
        import tempfile
        
        # Buat path thumbnail
        thumbnail_dir = os.path.join(tempfile.gettempdir(), 'youtube_downloader_thumbnails')
        os.makedirs(thumbnail_dir, exist_ok=True)
        
        # Nama file thumbnail berdasarkan nama video
        video_name = os.path.basename(video_path)
        thumbnail_path = os.path.join(thumbnail_dir, f"{os.path.splitext(video_name)[0]}.jpg")
        
        # Cek apakah thumbnail sudah ada
        if os.path.exists(thumbnail_path):
            return thumbnail_path
        
        # Buat thumbnail baru
        cap = cv2.VideoCapture(video_path)
        
        # Ambil frame ke-50 atau yang tersedia
        for i in range(50):
            ret, frame = cap.read()
            if not ret:
                break
        
        if ret:
            # Simpan thumbnail jika berhasil mengambil frame
            cv2.imwrite(thumbnail_path, frame)
            cap.release()
            return thumbnail_path
        else:
            cap.release()
            return None
    except ImportError:
        # Jika opencv tidak terinstall
        return None
    except Exception as e:
        print(f"Error creating thumbnail: {str(e)}")
        return None