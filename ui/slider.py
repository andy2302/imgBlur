from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt


def create_slider(min_val, max_val, default_val, on_change_callback):
    slider = QSlider(Qt.Horizontal)
    slider.setRange(min_val, max_val)
    slider.setValue(default_val)
    slider.valueChanged.connect(on_change_callback)
    return slider