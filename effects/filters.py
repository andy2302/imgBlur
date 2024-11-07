import cv2


def apply_gaussian_blur(image, intensity):
    ksize = 2 * intensity + 3
    return cv2.GaussianBlur(image, (ksize, ksize), 0)


def apply_median_blur(image, intensity):
    ksize = 2 * intensity + 3
    return cv2.medianBlur(image, ksize)


def apply_bilateral_blur(image, intensity):
    scale_factor = 0.5
    small_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
    ksize = 2 * intensity + 1
    sigma_color = sigma_space = ksize * 3
    blurred_small_image = cv2.bilateralFilter(small_image, ksize, sigma_color, sigma_space)
    return cv2.resize(blurred_small_image, (image.shape[1], image.shape[0]))


def apply_box_blur(image, intensity):
    ksize = max(3, intensity * 3)
    return cv2.blur(image, (ksize, ksize))
