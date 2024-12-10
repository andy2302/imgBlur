import cv2
import numpy as np


def adjust_temperature(image, delta):
    """Adjust the color temperature of the image."""
    blue, green, red = cv2.split(image)
    red = cv2.addWeighted(red, 1.0, red, 0, delta)
    blue = cv2.addWeighted(blue, 1.0, blue, 0, -delta)
    return cv2.merge((blue, green, red))


def adjust_tint(image, delta):
    """Adjust the tint of the image."""
    blue, green, red = cv2.split(image)
    green = cv2.addWeighted(green, 1.0, green, 0, delta)
    return cv2.merge((blue, green, red))


def adjust_exposure(image, delta):
    """Adjust the exposure of the image."""
    return cv2.convertScaleAbs(image, alpha=1.0 + delta / 100.0, beta=0)


def adjust_contrast(image, delta):
    """Adjust the contrast of the image."""
    return cv2.convertScaleAbs(image, alpha=1.0 + delta / 100.0, beta=0)


def adjust_highlights(image, delta):
    """Brighten highlights in the image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = np.clip(v + delta, 0, 255).astype(np.uint8)
    return cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)


def adjust_shadows(image, delta):
    """Brighten shadows in the image."""
    gamma = 1.0 + delta / 100.0
    invGamma = 1.0 / gamma
    lut = np.array([((i / 255.0) ** invGamma) * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image, lut)


def adjust_clarity(image, delta):
    """Add clarity by enhancing edges."""
    kernel = np.array([[0, -1, 0], [-1, 5 + delta / 10.0, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)


def adjust_saturation(image, delta):
    """Adjust the saturation of the image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = np.clip(s + delta, 0, 255).astype(np.uint8)
    return cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)


def adjust_sharpness(image, delta):
    """Sharpen the image."""
    kernel = np.array([[0, -1, 0], [-1, 5 + delta, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)


def reduce_noise(image, delta):
    """Reduce noise in the image."""
    return cv2.fastNlMeansDenoisingColored(image, None, delta, delta, 7, 21)


def reduce_moire(image):
    """Remove moire patterns (advanced filtering)."""
    return cv2.GaussianBlur(image, (9, 9), 0)


def defringe(image, delta):
    """Defringe by adjusting color fringes."""
    return cv2.addWeighted(image, 1.0, cv2.GaussianBlur(image, (5, 5), delta), -0.5, 128)
