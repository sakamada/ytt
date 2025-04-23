# ui/edit_tab.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QSlider, QFrame)
from PyQt5.QtCore import Qt, QSize, pyqtSlot, QUrl, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

import os

class EditTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.current_video = None
        self.init_ui()
        
    def init_ui(self):
        # Layout utama
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Area preview video
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(300)
        self.video_widget.setStyleSheet("background-color: #1a1a1a;")
        main_layout.addWidget(self.video_widget)

        # Media player untuk preview
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        
        # Connect signals dengan parameter yang tepat
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.stateChanged.connect(self.state_changed)
        
        # Kontrol video dan timeline
        controls_layout = QHBoxLayout()
        
        # Tombol play/pause
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("resources/play.png"))
        self.play_button.setIconSize(QSize(24, 24))
        self.play_button.clicked.connect(self.toggle_play)
        controls_layout.addWidget(self.play_button)
        
        # Timeline slider
        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setRange(0, 0)
        self.timeline.sliderMoved.connect(self.set_position)
        controls_layout.addWidget(self.timeline)
        
        # Label untuk waktu
        self.time_label = QLabel("00:00 / 00:00")
        controls_layout.addWidget(self.time_label)
        
        main_layout.addLayout(controls_layout)
        
        # Area editing
        edit_frame = QFrame()
        edit_frame.setStyleSheet("background-color: #2a2a2a; border-radius: 4px;")
        edit_layout = QVBoxLayout(edit_frame)
        
        # Judul section
        section_title = QLabel("Potong Video")
        section_title.setStyleSheet("font-weight: bold; color: white;")
        edit_layout.addWidget(section_title)
        
        # Tombol untuk memotong video
        split_button = QPushButton("Potong Video")
        split_button.clicked.connect(self.split_video)
        edit_layout.addWidget(split_button)
        
        main_layout.addWidget(edit_frame)
        main_layout.addStretch()

    def position_changed(self, position):
        """
        Slot yang dipanggil ketika posisi media player berubah
        
        Args:
            position (int): Posisi saat ini dalam milidetik
        """
        # Update timeline
        self.timeline.setValue(position)
        
        # Update label waktu
        current_time = QTime(0, 0)
        current_time = current_time.addMSecs(position)
        
        duration_time = QTime(0, 0)
        duration = self.media_player.duration()
        duration_time = duration_time.addMSecs(duration)
        
        time_format = "mm:ss" if duration < 3600000 else "hh:mm:ss"
        time_display = f"{current_time.toString(time_format)} / {duration_time.toString(time_format)}"
        
        self.time_label.setText(time_display)
        
    def duration_changed(self, duration):
        """
        Slot yang dipanggil ketika durasi media berubah
        
        Args:
            duration (int): Durasi media dalam milidetik
        """
        self.timeline.setRange(0, duration)
        
    def state_changed(self, state):
        """
        Slot yang dipanggil ketika status media player berubah
        
        Args:
            state (int): Status media player
        """
        if state == QMediaPlayer.PlayingState:
            self.play_button.setIcon(QIcon("resources/pause.png"))
        else:
            self.play_button.setIcon(QIcon("resources/play.png"))
            
    def toggle_play(self):
        """Toggle status play/pause media player"""
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
            
    def set_position(self, position):
        """
        Set posisi media player
        
        Args:
            position (int): Posisi yang diinginkan dalam milidetik
        """
        self.media_player.setPosition(position)
        
    def load_video(self, video_path):
        """
        Muat video ke media player
        
        Args:
            video_path (str): Path ke file video
        """
        self.current_video = video_path
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.play_button.setEnabled(True)
        
    def split_video(self):
        """Potong video berdasarkan posisi saat ini"""
        if not self.current_video:
            return
            
        # Implementasi pemotongan video bisa ditambahkan di sini
        # Misalnya, menggunakan self.api_client untuk memotong video
        pass
