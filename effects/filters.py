import cv2
import numpy as np


def validate_inputs(image, intensity):
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a valid NumPy array.")
    if not isinstance(intensity, int) or intensity < 1:
        raise ValueError("Intensity must be a positive integer greater than 0.")
    if image.size == 0:
        raise ValueError("Input image is empty.")


def apply_gaussian_blur(image, intensity):
    try:
        validate_inputs(image, intensity)
        ksize = 2 * intensity + 3
        return cv2.GaussianBlur(image, (ksize, ksize), 0)
    except Exception as e:
        print(f"Error in apply_gaussian_blur: {e}")
        return image


def apply_median_blur(image, intensity):
    try:
        validate_inputs(image, intensity)
        ksize = 2 * intensity + 3
        return cv2.medianBlur(image, ksize)
    except Exception as e:
        print(f"Error in apply_median_blur: {e}")
        return image


def apply_bilateral_blur(image, intensity):
    try:
        validate_inputs(image, intensity)
        scale_factor = 0.5
        small_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
        ksize = 2 * intensity + 1
        sigma_color = sigma_space = ksize * 3
        blurred_small_image = cv2.bilateralFilter(small_image, ksize, sigma_color, sigma_space)
        return cv2.resize(blurred_small_image, (image.shape[1], image.shape[0]))
    except Exception as e:
        print(f"Error in apply_bilateral_blur: {e}")
        return image


def apply_box_blur(image, intensity):
    try:
        validate_inputs(image, intensity)
        ksize = max(3, intensity * 3)
        return cv2.blur(image, (ksize, ksize))
    except Exception as e:
        print(f"Error in apply_box_blur: {e}")
        return image
