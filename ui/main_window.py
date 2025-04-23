# ui/main_window.py
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from ui.dashboard_tab import DashboardTab
from ui.edit_tab import EditTab
from services.api_client import ApiClient

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        
        # Inisialisasi API client
        self.api_client = ApiClient(config['backend_url'])
        
        # Setup dasar jendela
        self.setWindowTitle("YouTube Video Downloader & Editor")
        self.setMinimumSize(800, 600)
        
        # Inisialisasi UI
        self.init_ui()
    
    def init_ui(self):
        # Widget utama
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header dengan judul
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("background-color: #1a1a1a;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        
        title = QLabel("YouTube Video Downloader & Editor")
        title.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 16px;")
        header_layout.addWidget(title)
        
        # Tombol window controls (minimize, maximize, close)
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(5)
        
        # Tombol Sun/Moon untuk tema
        theme_btn = QPushButton()
        theme_btn.setObjectName("ThemeButton")
        theme_btn.setIcon(QIcon("resources/sun.png"))
        theme_btn.setFixedSize(30, 30)
        
        # Tombol folder
        folder_btn = QPushButton()
        folder_btn.setObjectName("FolderButton")
        folder_btn.setIcon(QIcon("resources/folder.png"))
        folder_btn.setFixedSize(30, 30)
        
        # Tombol minimize
        min_btn = QPushButton("-")
        min_btn.setObjectName("MinButton")
        min_btn.setFixedSize(30, 30)
        min_btn.clicked.connect(self.showMinimized)
        
        # Tombol maximize
        max_btn = QPushButton("□")
        max_btn.setObjectName("MaxButton")
        max_btn.setFixedSize(30, 30)
        max_btn.clicked.connect(self.toggle_maximize)
        
        # Tombol close
        close_btn = QPushButton("×")
        close_btn.setObjectName("CloseButton")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        
        controls_layout.addWidget(theme_btn)
        controls_layout.addWidget(folder_btn)
        controls_layout.addWidget(min_btn)
        controls_layout.addWidget(max_btn)
        controls_layout.addWidget(close_btn)
        
        header_layout.addStretch()
        header_layout.addLayout(controls_layout)
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setStyleSheet("QTabBar::tab { height: 30px; }")
        
        # Dashboard tab
        self.dashboard_tab = DashboardTab(self.api_client)
        self.tabs.addTab(self.dashboard_tab, "Dasbor")
        
        # Edit tab
        self.edit_tab = EditTab(self.api_client)
        self.tabs.addTab(self.edit_tab, "Edit")
        
        main_layout.addWidget(self.tabs)
        
        self.setCentralWidget(central_widget)
        
        # Remove default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def switch_to_edit_tab(self, video_path):
        """Switch to edit tab and load the specified video"""
        self.tabs.setCurrentIndex(1)  # Index 1 is Edit tab
        self.edit_tab.load_video(video_path)
    
    # Allow window dragging
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 50:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.y() < 50:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
