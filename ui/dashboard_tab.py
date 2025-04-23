# ui/dashboard_tab.py
import os
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QListWidget, QFrame, QSpinBox, 
                            QListWidgetItem, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from PyQt5.QtGui import QIcon

from services.video_item_widget import VideoItemWidget
from utils.file_manager import list_downloaded_videos

class DashboardTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.videos = []
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # URL input and buttons
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL here...")
        self.download_btn = QPushButton("Download")
        self.import_btn = QPushButton("Import Video")
        
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.download_btn)
        url_layout.addWidget(self.import_btn)
        
        # Connect buttons
        self.download_btn.clicked.connect(self.download_video)
        self.import_btn.clicked.connect(self.import_video)
        
        # Video list section
        video_section_label = QLabel("Imported/Downloaded Videos")
        video_section_label.setStyleSheet("color: white; font-weight: bold;")
        
        self.video_list_container = QWidget()
        self.video_list_layout = QVBoxLayout(self.video_list_container)
        self.video_list_layout.setContentsMargins(0, 0, 0, 0)
        self.video_list_layout.setSpacing(5)
        
        # Split results section
        split_results_label = QLabel("Split Video Results")
        split_results_label.setStyleSheet("color: white; font-weight: bold;")
        
        self.split_results = QListWidget()
        self.split_results.setStyleSheet("background-color: #333333; color: white;")
        self.split_results.setMinimumHeight(150)
        
        # Status bar
        self.status_bar = QLabel("Ready")
        self.status_bar.setStyleSheet("color: #AAAAAA;")
        
        # Add widgets to main layout
        main_layout.addLayout(url_layout)
        main_layout.addWidget(video_section_label)
        main_layout.addWidget(self.video_list_container)
        main_layout.addWidget(split_results_label)
        main_layout.addWidget(self.split_results)
        main_layout.addWidget(self.status_bar)
        
        # Set the styling for the whole tab
        self.setStyleSheet("""
            QWidget {
                background-color: #222222;
                color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
            }
            QComboBox, QSpinBox {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
            }
            QPushButton[objectName="remove_btn"] {
                background-color: #e74c3c;
            }
            QPushButton[objectName="remove_btn"]:hover {
                background-color: #c0392b;
            }
        """)
        
        # Test data - add some sample videos for demonstration
        self.add_video_to_list("the importance of consistency in weight loss.mp4", 
                               "C:/Users/roema/Downloads/the importance of consistency in weight loss.mp4")
        self.add_video_to_list("the moment i started seeing results.mp4", 
                               "C:/Users/roema/Downloads/the moment i started seeing results.mp4")
        self.add_video_to_list("zoom_in_1743851796.mp4", 
                               "C:/Users/roema/Downloads/zoom_in_1743851796.mp4")
    
    def add_video_to_list(self, name, path):
        """Add a video entry to the list with all necessary controls"""
        video_item = QWidget()
        video_layout = QHBoxLayout(video_item)
        video_layout.setContentsMargins(0, 5, 0, 5)
        
        # Video name
        video_name = QLabel(name)
        video_name.setStyleSheet("color: white; font-weight: bold;")
        
        # Path (smaller text)
        video_path = QLabel(path)
        video_path.setStyleSheet("color: #AAAAAA; font-size: 9pt;")
        
        # Container for video name and path
        video_info = QWidget()
        info_layout = QVBoxLayout(video_info)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(0)
        info_layout.addWidget(video_name)
        info_layout.addWidget(video_path)
        
        # Parts controls
        parts_label = QLabel("Parts:")
        parts_label.setStyleSheet("color: white;")
        
        parts_spinner = QSpinBox()
        parts_spinner.setRange(1, 10)
        parts_spinner.setValue(2)
        parts_spinner.setFixedWidth(50)
        
        # Buttons
        split_btn = QPushButton("Split")
        edit_btn = QPushButton("Edit")
        remove_btn = QPushButton("Remove")
        remove_btn.setObjectName("remove_btn")
        
        # Add widgets to video item layout
        video_layout.addWidget(video_info, 5)
        video_layout.addWidget(parts_label)
        video_layout.addWidget(parts_spinner)
        video_layout.addWidget(split_btn)
        video_layout.addWidget(edit_btn)
        video_layout.addWidget(remove_btn)
        
        # Connect button signals
        split_btn.clicked.connect(lambda: self.split_video(path, parts_spinner.value()))
        edit_btn.clicked.connect(lambda: self.edit_video(path))
        remove_btn.clicked.connect(lambda: self.remove_video(video_item))
        
        # Add the video item to the list
        self.video_list_layout.addWidget(video_item)
        
        # Add a line separator
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #444444;")
        self.video_list_layout.addWidget(line)
        
        # Save reference to video item
        self.videos.append({"widget": video_item, "path": path, "name": name})
    
    def download_video(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_bar.setText("Please enter a YouTube URL")
            return
            
        self.status_bar.setText(f"Downloading video from {url}...")
        # Here you would call your API client to actually download the video
        # For demonstration, let's just add a dummy video
        self.add_video_to_list(f"Video from {url[:20]}...", f"D:/APLIKASI/Dreamy.v1/downloads/video_{len(self.videos)}.mp4")
        self.url_input.clear()
        self.status_bar.setText("Download completed")
    
    def import_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Video", "", "Video Files (*.mp4 *.avi *.mkv *.mov)")
        if file_path:
            import os
            file_name = os.path.basename(file_path)
            self.add_video_to_list(file_name, file_path)
            self.status_bar.setText(f"Imported: {file_name}")
    
    def split_video(self, path, parts):
        self.status_bar.setText(f"Splitting video into {parts} parts...")
        # Add code here to actually split the video
        # For demonstration, just show a message
        QMessageBox.information(self, "Split Video", f"Video would be split into {parts} parts.\nImplementation pending.")
        self.status_bar.setText("Ready")
    
    def edit_video(self, path):
        self.status_bar.setText(f"Editing video: {path}")
        # Add code here to open the video editor
        # This would typically open another widget or dialog
    
    def remove_video(self, video_item):
        # Find and remove the video from our list
        for i, video in enumerate(self.videos):
            if video["widget"] == video_item:
                video_item.deleteLater()
                # Also delete the separator line that follows
                if i < len(self.videos) - 1:  # If not the last item
                    separator = self.video_list_layout.itemAt(self.video_list_layout.indexOf(video_item) + 1).widget()
                    if separator:
                        separator.deleteLater()
                self.videos.pop(i)
                self.status_bar.setText(f"Removed video: {video['name']}")
                break