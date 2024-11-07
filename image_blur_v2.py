import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QSlider, QFrame
)
from PySide6.QtCore import Qt, QPropertyAnimation
from PySide6.QtGui import QPixmap, QImage

# Import the filters
from effects.filters import apply_gaussian_blur, apply_median_blur, apply_bilateral_blur, apply_box_blur


class ImageFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Filter App")
        self.setGeometry(100, 100, 800, 600)

        # Initialize variables
        self.image = None
        self.original_image = None
        self.checkpoints = []
        self.active_filters = {
            'gaussian': False,
            'median': False,
            'bilateral': False,
            'box': False
        }

        # Main layout
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Toggle button for burger menu
        self.toggle_button = QPushButton("☰")
        self.toggle_button.setFixedSize(40, 40)
        self.toggle_button.clicked.connect(self.toggle_menu)

        # Add toggle button to separate frame
        toggle_button_frame = QFrame()
        toggle_button_layout = QVBoxLayout()
        toggle_button_layout.addWidget(self.toggle_button)
        toggle_button_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        toggle_button_frame.setLayout(toggle_button_layout)

        # Side menu
        self.menu_widget = QFrame()
        self.menu_widget.setFixedWidth(0)
        self.menu_widget.setStyleSheet("background-color: #333; color: white;")

        menu_layout = QVBoxLayout()
        self.menu_widget.setLayout(menu_layout)

        # Load Image Button
        load_image_button = QPushButton("Load Image")
        load_image_button.clicked.connect(self.load_image)
        menu_layout.addWidget(load_image_button)

        # Filter buttons
        self.gaussian_button = QPushButton("Gaussian Blur")
        self.median_button = QPushButton("Median Blur")
        self.bilateral_button = QPushButton("Bilateral Blur")
        self.box_button = QPushButton("Box Blur")

        # Set click actions for filters
        self.gaussian_button.clicked.connect(lambda: self.toggle_filter('gaussian', self.gaussian_button))
        self.median_button.clicked.connect(lambda: self.toggle_filter('median', self.median_button))
        self.bilateral_button.clicked.connect(lambda: self.toggle_filter('bilateral', self.bilateral_button))
        self.box_button.clicked.connect(lambda: self.toggle_filter('box', self.box_button))

        # Add buttons to layout
        for btn in (self.gaussian_button, self.median_button, self.bilateral_button, self.box_button):
            menu_layout.addWidget(btn)
            btn.setCheckable(True)

        # Slider for filter intensity
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(1, 20)
        self.blur_slider.setValue(5)
        self.blur_slider.valueChanged.connect(self.apply_active_filters)
        menu_layout.addWidget(self.blur_slider)

        # Undo Button
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo_last)
        menu_layout.addWidget(undo_button)

        # Image display area
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #222;")

        main_layout.addWidget(toggle_button_frame)
        main_layout.addWidget(self.menu_widget)
        main_layout.addWidget(self.image_label, 1)

        # Initialize animation for menu
        self.animation = QPropertyAnimation(self.menu_widget, b"minimumWidth")
        self.animation.setDuration(300)
        self.menu_open = False

    def toggle_menu(self):
        if self.menu_open:
            self.animation.setStartValue(200)
            self.animation.setEndValue(0)
            self.toggle_button.setText("☰")
        else:
            self.animation.setStartValue(0)
            self.animation.setEndValue(200)
            self.toggle_button.setText("×")
        self.menu_open = not self.menu_open
        self.animation.start()

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.original_image = self.image.copy()
            self.checkpoints = [self.image.copy()]
            self.show_image(self.image)

    def show_image(self, img):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def toggle_filter(self, filter_name, button):
        # Toggle filter on/off
        self.active_filters[filter_name] = not self.active_filters[filter_name]
        button.setChecked(self.active_filters[filter_name])
        self.apply_active_filters()

    def apply_active_filters(self):
        if self.image is not None:
            current_image = self.original_image.copy()
            intensity = self.blur_slider.value()

            # Apply active filters in sequence
            if self.active_filters['gaussian']:
                current_image = apply_gaussian_blur(current_image, intensity)
            if self.active_filters['median']:
                current_image = apply_median_blur(current_image, intensity)
            if self.active_filters['bilateral']:
                current_image = apply_bilateral_blur(current_image, intensity)
            if self.active_filters['box']:
                current_image = apply_box_blur(current_image, intensity)

            self.image = current_image
            self.checkpoints.append(current_image.copy())
            self.show_image(current_image)

    def undo_last(self):
        if len(self.checkpoints) > 1:
            self.checkpoints.pop()  # Remove the current state
            self.image = self.checkpoints[-1].copy()  # Revert to the previous state
            self.show_image(self.image)


# Main loop to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageFilterApp()
    window.show()
    sys.exit(app.exec())
