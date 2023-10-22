import os
import sys
import shutil

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

img_height, img_width = 512, 512
dataset_path = r"D:\3nethra-neo-data"
new_dataset_path = r"D:\NEW_ROP_DATA_REDUCED"

# create output directory
if not os.path.exists(new_dataset_path):
    os.mkdir(new_dataset_path)

new_patient_folders = os.listdir(new_dataset_path)
patient_folders = os.listdir(dataset_path)
total_patients = len(patient_folders)
patient_number = len(new_patient_folders)

for patient_folder in patient_folders:
    try:
        if patient_folder in new_patient_folders:
            continue
        new_patient_fp = os.path.join(new_dataset_path, patient_folder)
        os.mkdir(new_patient_fp)
        patient_folder_path = os.path.join(dataset_path, patient_folder)
        if not(os.path.isdir(patient_folder_path)):
            continue
        visit_folders = os.listdir(patient_folder_path)

        for visit_folder in visit_folders:
            new_visit_fp = os.path.join(new_patient_fp, visit_folder)
            os.mkdir(new_visit_fp)
            visit_folder_path = os.path.join(patient_folder_path, visit_folder)
            images = os.listdir(visit_folder_path)

            for image in images:
                new_image_path = os.path.join(new_visit_fp, image)
                image_name = image[:-4]
                image_path = os.path.join(visit_folder_path, image)
                try:
                    if image_name[-2:] != "TN" and image_name[0] != "." and image[-4:] == '.png':
                        #resize images
                        img = Image.open(image_path)
                        img = img.resize((img_height, img_width))
                        img.save(new_image_path)
                except OSError:
                    continue
                    
    except KeyboardInterrupt:
        print(f"Program terminated. Last opened directory: {patient_folder}")
        shutil.rmtree(new_patient_fp)
        sys.exit()

    print(f"{patient_number}/{total_patients} folders successfully copied")
    patient_number += 1

print("Done")