import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap


class ImageBlur(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the image variable
        self.image = None

        # Set up the GUI
        self.setWindowTitle('Image Blur')
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(0, 50)
        self.blur_slider.setValue(0)
        self.blur_slider.setTickInterval(5)
        self.blur_slider.setTickPosition(QSlider.TicksBelow)
        self.load_button = QPushButton('Load Image')
        self.gaussian_button = QPushButton('Gaussian Blur')
        self.median_button = QPushButton('Median Blur')
        self.bilateral_button = QPushButton('Bilateral Blur')
        self.box_button = QPushButton('Box Blur')
        self.original_button = QPushButton('Original Image')
        self.exit = QPushButton('Exit')
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.blur_slider)
        layout.addWidget(self.load_button)
        layout.addWidget(self.gaussian_button)
        layout.addWidget(self.median_button)
        layout.addWidget(self.bilateral_button)
        layout.addWidget(self.box_button)
        layout.addWidget(self.original_button)
        layout.addWidget(self.exit)
        self.setLayout(layout)

        # Connect the slider and buttons to the appropriate functions
        self.load_button.clicked.connect(self.open_image)
        self.gaussian_button.clicked.connect(self.gaussian_blur_image)
        self.median_button.clicked.connect(self.median_blur_image)
        self.bilateral_button.clicked.connect(self.bilateral_blur_image)
        self.box_button.clicked.connect(self.box_blur_image)
        self.original_button.clicked.connect(self.original_image)
        self.exit.clicked.connect(self.close)

    def open_image(self):
        # Open a file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')

        # If a file was selected, load the image
        if file_name:
            self.image = cv2.imread(file_name)
            self.show_image(self.image)

    def show_image(self, image):
        # Convert the image from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert the image to a QPixmap and display it
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        self.image_label.setPixmap(pixmap)

    def gaussian_blur_image(self):
        # If an image has been loaded, apply the Gaussian blur to the image
        if self.image is not None:
            blurred_image = cv2.GaussianBlur(self.image, (2 * self.blur_slider.value() + 1, 2 * self.blur_slider.value() + 1), 0)
            self.show_image(blurred_image)

    def median_blur_image(self):
        # If an image has been loaded, apply the Median blur to the image
        if self.image is not None:
            blurred_image = cv2.medianBlur(self.image, 2 * self.blur_slider.value() + 1)
            self.show_image(blurred_image)

    def bilateral_blur_image(self):
        # If an image has been loaded, apply the bilateral blur to the image
        if self.image is not None:
            scale_factor = 0.5  # reduce the size by half
            small_image = cv2.resize(self.image, None, fx=scale_factor, fy=scale_factor)
            kernel_size = 2 * self.blur_slider.value() + 1
            sigma_color = sigma_space = kernel_size // 6.0
            blurred_small_image = cv2.bilateralFilter(small_image, kernel_size, sigma_color, sigma_space)
            blurred_image = cv2.resize(blurred_small_image, (self.image.shape[1], self.image.shape[0]))
            self.show_image(blurred_image)

    def box_blur_image(self):
        # If an image has been loaded, apply the box blur to the image
        if self.image is not None:
            kernel_size = self.blur_slider.value()
            kernel = (kernel_size, kernel_size)
            blurred_image = cv2.blur(self.image, kernel)
            self.show_image(blurred_image)

    def original_image(self):
        self.show_image(self.image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageBlur()
    ex.show()
    sys.exit(app.exec_())

