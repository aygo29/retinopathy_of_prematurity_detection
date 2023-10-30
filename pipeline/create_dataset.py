# INPUT: DATA = folder containing .npy files in separate class folders
# OUTPUT: OUT = new folder containing 2 embedding files
import numpy as np
import os
import tensorflow as tf
from tqdm import tqdm

DATA = "INPUT DIRECTORY PATH"
NAME = "OUTPUT FILE NAME"
OUT = f"OUTPUT DIRECTORY PATH"

class_folders = sorted(os.listdir(DATA))
x = []
y = []

for i in tqdm(range(len(class_folders))):
    folder = class_folders[i]
    folder_path = os.path.join(DATA, folder)
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        embedding = np.load(file_path).transpose()
        x.append(embedding)
        y.append(i)

x = np.array(x)
y = tf.keras.utils.to_categorical(y, num_classes=len(class_folders))

if not os.path.exists(OUT):
    os.mkdir(OUT)
np.save(f"{OUT}{NAME}.npy", x)
np.save(f"{OUT}{NAME}_labels.npy", y)