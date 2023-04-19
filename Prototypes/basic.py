import cv2
from tkinter import filedialog

file_path = filedialog.askopenfilename()
# Load the image
img = cv2.imread(file_path)

# Apply a Gaussian blur with a kernel size of (15, 15)
blurred_img = cv2.GaussianBlur(img, (25, 25), 10)

# Show the original and blurred images side by side
cv2.imshow('Original', img)
cv2.imshow('Blurred', blurred_img)
cv2.waitKey(0)
