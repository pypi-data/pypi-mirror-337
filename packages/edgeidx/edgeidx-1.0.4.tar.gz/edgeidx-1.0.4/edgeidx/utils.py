import cv2
import os

def get_tessdata_prefix():
    return os.path.join(os.path.dirname(__file__), "..", "tessdata")

def adjust_contrast(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(image)

def remove_noise(image):
    return cv2.fastNlMeansDenoising(image, None, 30, 7, 21)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Error: Could not open or find the image!")
    
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contrast_img = adjust_contrast(gray_img)
    noise_free_img = remove_noise(contrast_img)
    blurred_img = cv2.GaussianBlur(noise_free_img, (5, 5), 0)

    return cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
