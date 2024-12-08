import cv2
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QFileDialog, QVBoxLayout, QFrame, QPushButton
from ui.menu import create_menu_widget
from ui.image_display import create_image_display
from ui.slider import create_slider
from effects.filters import apply_gaussian_blur, apply_median_blur, apply_bilateral_blur, apply_box_blur


class ImageFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Filter App")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Toggle button frame
        toggle_button_frame = QFrame()
        toggle_button_layout = QVBoxLayout()
        toggle_button_frame.setLayout(toggle_button_layout)

        # Add toggle menu button
        self.toggle_button = QPushButton("☰")
        self.toggle_button.setFixedSize(40, 40)
        self.toggle_button.clicked.connect(self.toggle_menu)
        toggle_button_layout.addWidget(self.toggle_button)

        toggle_button_layout.addStretch()

        # Create menu widget
        self.menu_widget, self.animation, self.menu_open = create_menu_widget(self)

        # Image display area
        self.image_label = create_image_display()

        # Add widgets to the main layout
        main_layout.addWidget(toggle_button_frame)  # Burger menu button always visible
        main_layout.addWidget(self.menu_widget)     # Collapsible menu
        main_layout.addWidget(self.image_label, 1)  # Image display takes remaining space

        # Initialize variables for image and filters
        self.image = None
        self.original_image = None
        self.checkpoints = []  # Initialize checkpoints
        self.active_filters = {}

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

    def toggle_blurs_menu(self):
        if self.blurs_menu.width() > 0:
            self.blurs_menu.setFixedWidth(0)
        else:
            self.blurs_menu.setFixedWidth(200)

    def toggle_adjustments_menu(self):
        if self.adjustments_menu.width() > 0:
            self.adjustments_menu.setFixedWidth(0)
        else:
            self.adjustments_menu.setFixedWidth(200)

    def reset_filters(self):
        self.active_filters = {key: False for key in self.active_filters}
        self.apply_active_filters()

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.original_image = self.image.copy()
            self.show_image(self.image)

    def undo_last(self):
        if self.checkpoints and len(self.checkpoints) > 1:
            self.checkpoints.pop()  # Remove the current state
            self.image = self.checkpoints[-1].copy()  # Revert to the previous state
            self.show_image(self.image)
        else:
            print("No more undo steps available.")

    def show_image(self, img):
        if img is not None:
            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(
                pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def apply_active_filters(self):
        if self.image is not None:
            current_image = self.original_image.copy()
            intensity = self.slider.value()

            # Apply active filters in sequence
            if self.active_filters.get('gaussian'):
                current_image = apply_gaussian_blur(current_image, intensity)
            if self.active_filters.get('median'):
                current_image = apply_median_blur(current_image, intensity)
            if self.active_filters.get('bilateral'):
                current_image = apply_bilateral_blur(current_image, intensity)
            if self.active_filters.get('box'):
                current_image = apply_box_blur(current_image, intensity)

            self.image = current_image
            self.checkpoints.append(current_image.copy())
            self.show_image(current_image)