# services/video_item_widget.py
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                           QLabel, QSpinBox, QSizePolicy, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

class VideoItemWidget(QWidget):
    # Signals
    split_requested = pyqtSignal(str, int)
    edit_requested = pyqtSignal(str)
    remove_requested = pyqtSignal(str, QListWidgetItem)
    
    def __init__(self, title, path):
        super().__init__()
        self.title = title
        self.path = path
        self.init_ui()
    
    def init_ui(self):
        # Layout utama
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Thumbnail dan info
        info_layout = QVBoxLayout()
        
        # Judul video
        title_label = QLabel(self.title)
        title_label.setStyleSheet("color: white; font-weight: bold;")
        title_label.setWordWrap(True)
        info_layout.addWidget(title_label)
        
        # Path video
        path_label = QLabel(self.path)
        path_label.setStyleSheet("color: #7f8c8d; font-size: 10px;")
        path_label.setWordWrap(True)
        info_layout.addWidget(path_label)
        
        main_layout.addLayout(info_layout, stretch=1)
        
        # Split controls
        split_layout = QHBoxLayout()
        
        parts_label = QLabel("Parts:")
        parts_label.setStyleSheet("color: white;")
        split_layout.addWidget(parts_label)
        
        self.parts_spinbox = QSpinBox()
        self.parts_spinbox.setMinimum(2)
        self.parts_spinbox.setMaximum(10)
        self.parts_spinbox.setValue(2)
        self.parts_spinbox.setFixedWidth(50)
        split_layout.addWidget(self.parts_spinbox)
        
        split_button = QPushButton("Split")
        split_button.setFixedWidth(70)
        split_button.clicked.connect(self.on_split_clicked)
        split_layout.addWidget(split_button)
        
        main_layout.addLayout(split_layout)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        
        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(70)
        edit_button.clicked.connect(self.on_edit_clicked)
        actions_layout.addWidget(edit_button)
        
        remove_button = QPushButton("Remove")
        remove_button.setObjectName("RedButton")
        remove_button.setFixedWidth(70)
        remove_button.clicked.connect(self.on_remove_clicked)
        actions_layout.addWidget(remove_button)
        
        main_layout.addLayout(actions_layout)
        
        # Set fixed height for consistent appearance
        self.setFixedHeight(70)
    
    @pyqtSlot()
    def on_split_clicked(self):
        parts = self.parts_spinbox.value()
        self.split_requested.emit(self.path, parts)
    
    @pyqtSlot()
    def on_edit_clicked(self):
        self.edit_requested.emit(self.path)
    
    @pyqtSlot()
    def on_remove_clicked(self):
        self.remove_requested.emit(self.path, self.parentWidget().currentItem())