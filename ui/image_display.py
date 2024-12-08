from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


def create_image_display():
    image_label = QLabel()
    image_label.setAlignment(Qt.AlignCenter)
    image_label.setStyleSheet("background-color: #222;")
    image_label.setText("No image loaded")
    return image_label