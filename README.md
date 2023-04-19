# Image Blur

Image Blur is a simple desktop application that allows you to apply different types of blur effects to your images. The application is built using Python, OpenCV, and PyQt5. With a user-friendly interface, you can easily load an image, adjust the intensity of the blur, and apply various blur effects, such as Gaussian blur, Median blur, Bilateral blur, and Box blur. You can also view the original image at any time.

## Features

* Load and display images (supports .png, .jpg, .jpeg, and .bmp formats)
* Apply Gaussian blur, Median blur, Bilateral blur, and Box blur effects, etc.
* Adjust the intensity of the blur using a slider
* View the original image
* Exit the application

## Prerequisites

Before running the application, you need to have the following software installed:

* Python 3.x
* OpenCV
* PyQt5

To install the required packages, you can use the following commands:

`pip install opencv-python`

`pip install PyQt5`

## Usage

1. Clone this repository or download the source code.
2. Navigate to the folder containing the source code.
3. Run the script using the following command:
python `python image_blur.py`
4. The application window will open. Click the "Load Image" button to open an image.
5. Use the slider to adjust the intensity of the blur effect.
6. Click on the desired blur effect button to apply the effect on the image.
7. To view the original image, click the "Original Image" button.
8. To exit the application, click the "Exit" button.

## Code Explanation

#### Imports

```
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
```
* **import sys**: Imports the sys module, which is used to interact with the Python runtime environment.
* **import cv2**: Imports the OpenCV library, which provides image processing functions.
* **from PyQt5.QtWidgets ...**: Imports various PyQt5 widgets that will be used to create the graphical user interface.
* **from PyQt5.QtCore import Qt**: Imports the Qt class, which contains core non-graphical functionality.
* **from PyQt5.QtGui import QImage, QPixmap**: Imports QImage and QPixmap classes, which are used to work with images in the application.

#### ImageBlur Class
```
class ImageBlur(QWidget):
    def __init__(self):
        super().__init__()
```
* Defines the **ImageBlur** class, which inherits from **QWidget**.
* The `__init__` method is the constructor, and the `super().__init__()` call initializes the parent class, **QWidget**.

#### Initialize Image Variable
        `self.image = None`
* Initializes the **image** variable to **None**, which will later store the loaded image.

#### Set up GUI

        self.setWindowTitle('Image Blur')
        self.setFixedSize(1675, 920)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.blur_slider = QSlider(Qt.Horizontal)
        ...
        layout.addWidget(self.exit)
        self.setLayout(layout)
* Sets up the graphical user interface by creating various widgets (e.g., labels, buttons, sliders) and configuring their properties.
* Adds the widgets to a vertical layout, and sets this layout for the **ImageBlur** class.

#### Connect Slider and Buttons to Functions

        self.load_button.clicked.connect(self.open_image)
        ...
        self.exit.clicked.connect(self.close)
* Connects the slider and buttons to their corresponding functions. These functions will be executed when the buttons are clicked or the slider is adjusted.

#### Open Image Function

    def open_image(self):
        ...
        if file_name:
            self.image = cv2.imread(file_name)
            self.show_image(self.image)
* Opens a file dialog to select an image file.
* If a file is selected, the image is loaded using OpenCV's `imread()` function and displayed using the `show_image()` method.

#### Show Image Function

    def show_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        self.image_label.setPixmap(pixmap)
* Converts the input image from BGR to RGB color space using OpenCV's `cvtColor()` function.
* Creates a `QImage` object from the image data, and then creates a `QPixmap` object from the `QImage`.
* Sets the `QPixmap` as the pixmap of the `image_label` widget, which displays the image.

#### Blur Functions

    def gaussian_blur_image(self):
        ...
    def median_blur_image(self):
        ...
    def bilateral_blur_image(self):
        ...
    def box_blur_image(self):
        ...
* These four functions apply Gaussian, Median, Bilateral, and Box blur effects to the image, respectively.

Each function checks if an image has been loaded (**if self.image is not None**).
Then, the functions apply the corresponding blur effect using OpenCV functions, such as **cv2.GaussianBlur()**, **cv2.medianBlur()**, **cv2.bilateralFilter()**, and **cv2.blur()**.
The blur intensity is controlled by the slider value (**self.blur_slider.value()**).
Once the blurred image is generated, it is displayed using the **show_image()** method.

#### Original Image Function

    def original_image(self):
        self.show_image(self.image)
This function simply calls the `show_image()` method with the original image, effectively displaying the original image without any blur effect.

#### Main Block

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = ImageBlur()
        ex.show()
        sys.exit(app.exec_())
* This block of code is executed when the script is run directly (not imported as a module).
* It creates a **QApplication** instance, passing in the command-line arguments.
* It then creates an instance of the **ImageBlur** class, displays the application window using the `show()` method, and starts the event loop with `app.exec_()`.
* The `sys.exit()` call ensures a clean exit when the application is closed.

This covers the entire code of the Image Blur application. The code is organized into a single class that inherits from QWidget, with functions that handle different aspects of the application's behavior, such as loading images, applying blur effects, and displaying images. The GUI is created using PyQt5, and image processing is done using OpenCV.

## Contributing

I welcome contributions to improve this project. If you'd like to contribute, please feel free to create a fork and submit a pull request.

## License

This project is released under the MIT License.