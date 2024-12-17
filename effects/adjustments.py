import cv2
import numpy as np


def adjust_temperature(image, delta):
    """Adjust the color temperature of the image."""
    try:
        blue, green, red = cv2.split(image)
        red = cv2.addWeighted(red, 1.0, red, 0, delta)
        blue = cv2.addWeighted(blue, 1.0, blue, 0, -delta)
        print(f"Adjusting temperature with delta: {delta}")
        return cv2.merge((blue, green, red))
    except Exception as e:
        print(f"Error in adjust_temperature: {e}")
        return image


def adjust_tint(image, delta):
    """Adjust the tint of the image."""
    try:
        blue, green, red = cv2.split(image)
        green = cv2.addWeighted(green, 1.0, green, 0, delta)
        print(f"Adjusting tint with delta: {delta}")
        return cv2.merge((blue, green, red))
    except Exception as e:
        print(f"Error in adjust_tint: {e}")
        return image


def adjust_exposure(image, delta):
    """Adjust the exposure of the image."""
    try:
        print(f"Adjusting exposure with delta: {delta}")
        return cv2.convertScaleAbs(image, alpha=1.0 + delta / 100.0, beta=0)
    except Exception as e:
        print(f"Error in adjust_exposure: {e}")
        return image


def adjust_contrast(image, delta):
    """Adjust the contrast of the image."""
    try:
        print(f"Adjusting contrast with delta: {delta}")
        return cv2.convertScaleAbs(image, alpha=1.0 + delta / 100.0, beta=0)
    except Exception as e:
        print(f"Error in adjust_contrast: {e}")
        return image


def adjust_highlights(image, delta):
    """Brighten highlights in the image."""
    try:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = np.clip(v + delta, 0, 255).astype(np.uint8)
        print(f"Adjusting highlights with delta: {delta}")
        return cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)
    except Exception as e:
        print(f"Error in adjust_highlights: {e}")
        return image


def adjust_shadows(image, delta):
    """Brighten shadows in the image."""
    try:
        gamma = 1.0 + delta / 100.0
        invGamma = 1.0 / gamma
        lut = np.array([((i / 255.0) ** invGamma) * 255 for i in range(256)]).astype("uint8")
        print(f"Adjusting shadows with delta: {delta}")
        return cv2.LUT(image, lut)
    except Exception as e:
        print(f"Error in adjust_shadows: {e}")
        return image


def adjust_clarity(image, delta):
    """Add clarity by enhancing edges."""
    try:
        kernel = np.array([[0, -1, 0], [-1, 5 + delta / 10.0, -1], [0, -1, 0]])
        print(f"Adjusting clarity with delta: {delta}")
        return cv2.filter2D(image, -1, kernel)
    except Exception as e:
        print(f"Error in adjust_clarity: {e}")
        return image


def adjust_saturation(image, delta):
    """Adjust the saturation of the image."""
    try:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = np.clip(s + delta, 0, 255).astype(np.uint8)
        print(f"Adjusting saturation with delta: {delta}")
        return cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)
    except Exception as e:
        print(f"Error in adjust_saturation: {e}")
        return image


def adjust_sharpness(image, delta):
    """Sharpen the image without affecting exposure or intensity."""
    try:
        if delta == 0:
            print(f"No sharpening applied. Delta: {delta}")
            return image

        # Base kernel for edge enhancement
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])

        # Extract the edge details using the sharpening kernel
        edges = cv2.filter2D(image, -1, kernel)

        # Blend the edges back into the original image with controlled intensity
        sharpness_strength = delta / 50.0  # Adjust this scaling factor as needed
        sharpened = cv2.addWeighted(image, 1.0, edges - image, sharpness_strength, 0)

        print(f"Adjusting sharpness with delta: {delta}")
        return np.clip(sharpened, 0, 255).astype(np.uint8)
    except Exception as e:
        print(f"Error in adjust_sharpness: {e}")
        return image


def reduce_noise(image, delta):
    """Reduce noise in the image."""
    try:
        print(f"Reducing noise with delta: {delta}")
        return cv2.fastNlMeansDenoisingColored(image, None, delta, delta, 7, 21)
    except Exception as e:
        print(f"Error in reduce_noise: {e}")
        return image


def reduce_moire(image):
    """Remove moire patterns (advanced filtering)."""
    try:
        print("Reducing moire patterns.")
        return cv2.GaussianBlur(image, (9, 9), 0)
    except Exception as e:
        print(f"Error in reduce_moire: {e}")
        return image


def defringe(image, delta):
    """Defringe by adjusting color fringes."""
    try:
        print(f"Defringing with delta: {delta}")
        return cv2.addWeighted(image, 1.0, cv2.GaussianBlur(image, (5, 5), delta), -0.5, 128)
    except Exception as e:
        print(f"Error in defringe: {e}")
        return image