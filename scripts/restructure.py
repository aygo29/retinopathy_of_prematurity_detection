import os
import shutil
import pandas as pd

DATA = "../../dataset/NK_TEAM_IMAGES_BACK_UP_REDUCED/"
OUT = "../../dataset/rop_images/"
CSV = "../../dataset/csv/rop_images.csv"

if not os.path.exists(OUT):
    os.mkdir(OUT)

csv_data = {"file_name":[], "visit_folder":[], "patient_folder":[]}

for patient in os.listdir(DATA):
    patient_path = os.path.join(DATA, patient)
    for visit in os.listdir(patient_path):
        visit_path = os.path.join(patient_path, visit)
        for file in os.listdir(visit_path):
            file_path = os.path.join(visit_path, file)

            shutil.copy(file_path, OUT)
            csv_data["file_name"].append(file)
            csv_data["visit_folder"].append(visit)
            csv_data["patient_folder"].append(patient)

df = pd.DataFrame(csv_data)
df.to_csv(CSV)

file_count = len(os.listdir(OUT))
print(f"{file_count} files added to output folder.")
print(df.head())
