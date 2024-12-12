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
from effects.adjustments import adjust_temperature, adjust_tint, adjust_saturation, adjust_sharpness, adjust_contrast, \
    adjust_clarity, adjust_highlights, adjust_shadows, adjust_exposure, reduce_moire, reduce_noise, defringe


class ImageFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        print("Initializing application...")

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

        self.active_filters.update({
            'temperature': False, 'tint': False, 'exposure': False, 'contrast': False,
            'highlights': False, 'shadows': False, 'clarity': False, 'saturation': False,
            'sharpness': False, 'noise': False, 'moire': False, 'defringe': False
        })

        self.previous_adjustments = {  # Initialize with None to detect the first change
            "Temperature": None,
            "Tint": None,
            "Exposure": None,
            "Contrast": None,
            "Highlights": None,
            "Shadows": None,
            "Clarity": None,
            "Saturation": None,
            "Sharpness": None,
            "Noise": None,
            "Moire": None,
            "Defringe": None
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

        toggle_button_layout.addStretch()

        # Reset button
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_image)
        reset_button.setFixedSize(60, 30)
        toggle_button_layout.addWidget(reset_button)

        # Exit button
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        exit_button.setFixedSize(60, 30)
        toggle_button_layout.addWidget(exit_button)

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

        # Category Buttons
        blurs_button = QPushButton("Blurs")
        adjustments_button = QPushButton("Adjustments")

        # Add buttons to menu layout
        menu_layout.addWidget(blurs_button)
        menu_layout.addWidget(adjustments_button)

        # Submenu for Blurs
        self.blurs_menu = QFrame()
        self.blurs_menu.setStyleSheet("background-color: #555; color: white;")
        self.blurs_menu.setFixedWidth(0)  # Start hidden
        self.blurs_animation = QPropertyAnimation(self.blurs_menu, b"minimumWidth")
        self.blurs_animation.setDuration(300)

        blurs_menu_layout = QVBoxLayout()
        self.blurs_menu.setLayout(blurs_menu_layout)

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

        # Add buttons to submenu layout
        for btn in (self.gaussian_button, self.median_button, self.bilateral_button, self.box_button):
            blurs_menu_layout.addWidget(btn)
            btn.setCheckable(True)

        # Slider for filter intensity
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(1, 20)
        self.blur_slider.setValue(5)
        self.blur_slider.valueChanged.connect(self.apply_active_filters)
        blurs_menu_layout.addWidget(self.blur_slider)

        # Toggle blurs submenu visibility
        blurs_button.clicked.connect(self.toggle_blurs_menu)

        # Submenu for Adjustments
        self.adjustments_menu = QFrame()
        self.adjustments_menu.setStyleSheet("background-color: #555; color: white;")
        self.adjustments_menu.setFixedWidth(0)  # Start hidden
        self.adjustments_animation = QPropertyAnimation(self.adjustments_menu, b"minimumWidth")
        self.adjustments_animation.setDuration(300)

        adjustments_menu_layout = QVBoxLayout()
        self.adjustments_menu.setLayout(adjustments_menu_layout)

        # Adjustments Sliders
        self.adjustments_sliders = {}

        # Define adjustment parameters
        adjustments = [
            ("Temperature", -100, 100, 0),
            ("Tint", -100, 100, 0),
            ("Exposure", -100, 100, 0),
            ("Contrast", -100, 100, 0),
            ("Highlights", -100, 100, 0),
            ("Shadows", -100, 100, 0),
            ("Clarity", -100, 100, 0),
            ("Saturation", -100, 100, 0),
            ("Sharpness", -100, 100, 0),
            ("Noise", 0, 100, 0),
            ("Moire", 0, 1, 0),  # Treat moire as a toggle (0 or 1)
            ("Defringe", 0, 100, 0),
        ]

        # Add sliders for each adjustment
        for name, min_val, max_val, default in adjustments:
            label = QLabel(name)
            adjustments_menu_layout.addWidget(label)

            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(default)
            slider.valueChanged.connect(lambda value, n=name: self.update_adjustment(n, value))
            adjustments_menu_layout.addWidget(slider)

            # Label to show current value
            value_label = QLabel(f"{default}")
            adjustments_menu_layout.addWidget(value_label)

            # Store the slider and value label in a dictionary
            self.adjustments_sliders[name] = (slider, value_label)

        # Connect adjustments menu toggle
        adjustments_button.clicked.connect(self.toggle_adjustments_menu)

        # Add Undo button under Adjustments category
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo_last)
        menu_layout.addWidget(undo_button)

        # Add both menus to the main layout
        main_layout.addWidget(toggle_button_frame)
        main_layout.addWidget(self.menu_widget)
        main_layout.addWidget(self.blurs_menu)
        main_layout.addWidget(self.adjustments_menu)

        # Image display area
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #222;")
        main_layout.addWidget(self.image_label, 1)

        # Initialize animation for menu
        self.animation = QPropertyAnimation(self.menu_widget, b"minimumWidth")
        self.animation.setDuration(300)
        self.menu_open = False

    def toggle_blurs_menu(self):
        try:
            print("Toggling blurs menu...")
            if self.blurs_menu.width() > 0:
                self.blurs_animation.setStartValue(200)
                self.blurs_animation.setEndValue(0)
            else:
                self.blurs_animation.setStartValue(0)
                self.blurs_animation.setEndValue(200)
            self.blurs_animation.start()
        except Exception as e:
            print(f"Error toggling blurs menu: {e}")

    def toggle_adjustments_menu(self):
        try:
            print("Toggling adjustments menu...")
            if self.adjustments_menu.width() > 0:
                self.adjustments_animation.setStartValue(self.adjustments_menu.width())
                self.adjustments_animation.setEndValue(0)
            else:
                self.adjustments_animation.setStartValue(self.adjustments_menu.width())
                self.adjustments_animation.setEndValue(200)  # Adjust this value based on the desired width
            self.adjustments_animation.start()
        except Exception as e:
            print(f"Error toggling adjustments menu: {e}")

    def reset_image(self):
        try:
            print("Resetting image...")
            if self.original_image is not None:
                self.image = self.original_image.copy()
                self.checkpoints = [self.image.copy()]

                # Reset active filters
                self.active_filters = {key: False for key in self.active_filters}

                # Reset adjustment sliders
                for adjustment, (slider, value_label) in self.adjustments_sliders.items():
                    slider.setValue(0)
                    value_label.setText("0")

                # Reset filter buttons to unchecked state
                for button in [self.gaussian_button, self.median_button, self.bilateral_button, self.box_button]:
                    button.setChecked(False)

                # Clear previous adjustments tracking
                self.previous_adjustments = {key: None for key in self.previous_adjustments}

                # Show the original image
                self.show_image(self.image)
            else:
                print("No image to reset.")
        except Exception as e:
            print(f"Error resetting image: {e}")

    def toggle_menu(self):
        try:
            print("Toggling side menu...")
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
        except Exception as e:
            print(f"Error toggling menu: {e}")

    def load_image(self):
        try:
            print("Loading image...")
            file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
            if file_name:
                self.image = cv2.imread(file_name)
                if self.image is None:
                    raise ValueError("Failed to load image. Check the file format or path.")
                self.original_image = self.image.copy()
                self.checkpoints = [self.image.copy()]
                print(f"Image loaded: {file_name}")
                self.show_image(self.image)
        except Exception as e:
            print(f"Error loading image: {e}")

    def show_image(self, img):
        try:
            print("Displaying image...")
            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            print(f"Error displaying image: {e}")

    def toggle_filter(self, filter_name, button):
        try:
            print(f"Toggling filter: {filter_name}")
            self.active_filters[filter_name] = not self.active_filters[filter_name]
            button.setChecked(self.active_filters[filter_name])
            self.apply_active_filters()
        except Exception as e:
            print(f"Error toggling filter {filter_name}: {e}")

    def apply_active_filters(self):
        try:
            print("Applying active filters...")
            if self.image is not None:
                # Start with the original image to prevent accumulating changes
                current_image = self.original_image.copy()

                # Apply active blur filters
                intensity = self.blur_slider.value()
                if self.active_filters['gaussian']:
                    current_image = apply_gaussian_blur(current_image, intensity)
                if self.active_filters['median']:
                    current_image = apply_median_blur(current_image, intensity)
                if self.active_filters['bilateral']:
                    current_image = apply_bilateral_blur(current_image, intensity)
                if self.active_filters['box']:
                    current_image = apply_box_blur(current_image, intensity)

                # Apply adjustments cumulatively based on the sliders' values
                for adjustment, (slider, _) in self.adjustments_sliders.items():
                    value = slider.value()

                    # Apply the corresponding adjustment
                    if value != 0:  # Skip adjustments with zero values
                        print(f"Applying {adjustment} with value: {value}")
                        if adjustment == "Temperature":
                            current_image = adjust_temperature(current_image, value)
                        elif adjustment == "Tint":
                            current_image = adjust_tint(current_image, value)
                        elif adjustment == "Exposure":
                            current_image = adjust_exposure(current_image, value)
                        elif adjustment == "Contrast":
                            current_image = adjust_contrast(current_image, value)
                        elif adjustment == "Highlights":
                            current_image = adjust_highlights(current_image, value)
                        elif adjustment == "Shadows":
                            current_image = adjust_shadows(current_image, value)
                        elif adjustment == "Clarity":
                            current_image = adjust_clarity(current_image, value)
                        elif adjustment == "Saturation":
                            current_image = adjust_saturation(current_image, value)
                        elif adjustment == "Sharpness":
                            current_image = adjust_sharpness(current_image, value)
                        elif adjustment == "Noise":
                            current_image = reduce_noise(current_image, value)
                        elif adjustment == "Moire" and value > 0:
                            current_image = reduce_moire(current_image)
                        elif adjustment == "Defringe":
                            current_image = defringe(current_image, value)

                # Update the displayed image
                self.image = current_image
                self.checkpoints.append(current_image.copy())
                self.show_image(current_image)
        except Exception as e:
            print(f"Error applying filters: {e}")

    def update_adjustment(self, adjustment, value):
        try:
            print(f"Updating adjustment: {adjustment} with value {value}")
            slider, value_label = self.adjustments_sliders[adjustment]
            value_label.setText(f"{value}")
            self.apply_active_filters()
        except Exception as e:
            print(f"Error updating adjustment {adjustment}: {e}")

    def undo_last(self):
        try:
            print("Undoing last action...")
            if len(self.checkpoints) > 1:
                self.checkpoints.pop()  # Remove the current state
                self.image = self.checkpoints[-1].copy()  # Revert to the previous state
                self.show_image(self.image)
            else:
                print("No more actions to undo.")
        except Exception as e:
            print(f"Error undoing last action: {e}")


# Main loop to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageFilterApp()
    window.show()
    sys.exit(app.exec())