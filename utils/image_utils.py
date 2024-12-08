from PySide6.QtGui import QImage, QPixmap


def convert_cv_to_qt(img):
    height, width, channel = img.shape
    bytes_per_line = 3 * widthi
    q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_BGR888)
    return QPixmap.fromImage(q_img)
