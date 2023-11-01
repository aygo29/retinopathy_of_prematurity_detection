# INPUT: EMB_CSV = csv containing metadata of all 80k .npy files
# LAB_CSV = csv containing class labels of each visit
# DATA = folder containing all 80k embeddings
# LAB_COL = column name in LAB_CSV to be used for labelling
# OUTPUT: OUT = new folder containing 2 embedding files
import numpy as np
import os
import pandas as pd
import tensorflow as tf
from tqdm import tqdm

EMB_CSV = "../Other/rop_embeddings.csv"
LAB_CSV = "../Other/staging_annotations.csv"
DATA = "../../data/rop_enh_embeddings/"
LAB_COL = "LS"

NAME = "stage_clf_enh"
OUT = f"../../data/embeddings/"

data_df = pd.read_csv(EMB_CSV)
label_df = pd.read_csv(LAB_CSV)

classes = sorted(label_df[LAB_COL].unique())
num_classes = len(classes)
class_map = {}
for i in range(len(classes)):
    class_map[classes[i]] = i

for i in tqdm(range(len(data_df))):
    data_df.at[i, 'visit_folder'] = str(data_df.at[i, 'visit_folder'])[:8]

x = []
y = []

for i in tqdm(range(len(label_df))):
    patient_id = label_df.at[i, 'MRD']
    date = label_df.at[i, 'Date of visit']
    visit_id = "".join(date.split('-'))
    label = label_df.at[i, LAB_COL]
    class_ind = class_map[label]

    files = data_df[(data_df['patient_folder']==patient_id) & (data_df['visit_folder']==visit_id)]['file_name'].unique()
    for j in range(len(files)):
        file = files[j]
        file_path = os.path.join(DATA, file)
        embedding = np.load(file_path).transpose()
        x.append(embedding)
        y.append(class_ind)

x = np.array(x)
y = tf.keras.utils.to_categorical(y, num_classes=num_classes)

if not os.path.exists(OUT):
    os.mkdir(OUT)
np.save(f"{OUT}{NAME}.npy", x)
np.save(f"{OUT}{NAME}_labels.npy", y)