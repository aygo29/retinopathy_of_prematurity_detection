# INPUT: DATA = folder containing all 80k images
# OUTPUT: OUT = new folder containing enhanced 80k images
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Input directory containing subfolders with images
DATA = "INPUT DIRECTORY PATH"
OUT = "OUTPUT DIRECTORY PATH"

def my_PreProc(data):
    assert len(data.shape) == 4
    assert data.shape[3] == 3  # Check for 3 channels (RGB)

    # My preprocessing:
    data = dataset_normalized(data)
    data = clahe_equalized(data)
    data = adjust_gamma(data, 1.2)
    data = data / 255.  # Reduce to 0-1 range
    return data

# Normalize over the dataset
def dataset_normalized(imgs):
    imgs_normalized = np.empty(imgs.shape)
    for i in range(imgs.shape[0]):
        imgs_normalized[i] = ((imgs[i] - np.min(imgs[i])) / (np.max(imgs[i]) - np.min(imgs[i]))) * 255
    return imgs_normalized

# CLAHE (Contrast Limited Adaptive Histogram Equalization) for each channel
def clahe_equalized(imgs):
    assert len(imgs.shape) == 4  # 4D arrays
    assert imgs.shape[3] == 3  # Check for 3 channels (RGB)

    # Create a CLAHE object (Arguments are optional).
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    imgs_equalized = np.empty(imgs.shape)

    for i in range(imgs.shape[0]):
        for c in range(3):
            # Convert to 8-bit for CLAHE (assuming the input images are 8-bit)
            img_8bit = imgs[i][:, :, c].astype(np.uint8)
            imgs_equalized[i][:, :, c] = clahe.apply(img_8bit)

    return imgs_equalized

# Adjust gamma for each channel
def adjust_gamma(imgs, gamma=1.0):
    new_imgs = np.empty(imgs.shape)
    for i in range(imgs.shape[0]):
        for c in range(3):
            new_imgs[i][:, :, c] = cv2.LUT(np.array(imgs[i][:, :, c], dtype=np.uint8), create_gamma_lut(gamma))
    return new_imgs

# Create a lookup table mapping pixel values [0, 255] to adjusted gamma values
def create_gamma_lut(gamma=1.0):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
    return table

os.makedirs(OUT, exist_ok=True)

# Collect image files in the subfolder
image_files = [f for f in os.listdir(DATA) if f.endswith('.png')]

for i in tqdm(range(len(image_files))):
    image = image_files[i]
    output_image_path = os.path.join(OUT, image)
    if os.path.exists(output_image_path):
        continue

    image_path = os.path.join(DATA, image)
    img = cv2.imread(image_path)
    img = np.array([img])
    preprocessed_image = my_PreProc(img)[0]

    # Save preprocessed images in the output subfolder
    plt.imsave(output_image_path, preprocessed_image, cmap='gray')
