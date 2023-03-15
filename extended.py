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
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.blur_slider)
        layout.addWidget(self.load_button)
        self.setLayout(layout)

        # Connect the slider and button to the appropriate functions
        self.blur_slider.valueChanged.connect(self.blur_image)
        self.load_button.clicked.connect(self.open_image)

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

    def blur_image(self, amount):
        # If an image has been loaded, apply the blur to the image
        if self.image is not None:
            blurred_image = cv2.GaussianBlur(self.image, (2 * amount + 1, 2 * amount + 1), 0)
            self.show_image(blurred_image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageBlur()
    ex.show()
    sys.exit(app.exec_())
