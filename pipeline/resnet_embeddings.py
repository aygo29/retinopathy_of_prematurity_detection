# INPUT: DIR = folder containing all 80k images
# OUTPUT: OUT = new folder containing 80k embedding files

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet import preprocess_input
from tensorflow.keras.models import Model
import numpy as np
import os
from tqdm import tqdm

DIR = "INPUT DIRECTORY PATH"
OUT = "OUTPUT DIRECTORY PATH"
IMG_SIZE = 224

if not os.path.exists(OUT):
    os.mkdir(OUT)

base_model = ResNet50(weights='imagenet')
layer_name = "avg_pool"
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer_name).output)

def preprocess_image(path):
    img = image.load_img(path, target_size=(IMG_SIZE, IMG_SIZE))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

files = os.listdir(DIR)

for i in tqdm(range(len(files))):
    file_name = files[i]
    img_id = file_name.split('.png')[0]
    img_path = os.path.join(DIR, file_name)
    emb_path = os.path.join(OUT, img_id+'.npy')

    if os.path.exists(emb_path):
        continue
    
    try:
        x = preprocess_image(img_path)
        features = model.predict(x)
        np.save(emb_path, features)
    except OSError:
        pass