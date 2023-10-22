import os
import sys

new_dataset_path = r"D:\NK_TEAM_IMAGES_BACK_UP_REDUCED"
dataset_path = r"D:\NK_TEAM_IMAGES_BACK_UP_FROM_01-05-2022_TO_30-11-2022"

patient_folders = os.listdir(dataset_path)
new_patient_folders = os.listdir(new_dataset_path)
total_patients = len(patient_folders)
copied_patients = len(new_patient_folders)

def run_check():
    for patient_folder in patient_folders:
        patient_fp = os.path.join(dataset_path, patient_folder)
        new_patient_fp = os.path.join(new_dataset_path, patient_folder)
        if patient_folder not in new_patient_folders:
            print(f"{patient_fp} is missing")
            continue
        visit_folders = os.listdir(patient_fp)
        new_visit_folders = os.listdir(new_patient_fp)

        for visit_folder in visit_folders:
            visit_fp = os.path.join(patient_fp, visit_folder)
            new_visit_fp = os.path.join(new_patient_fp, visit_folder)
            if visit_folder not in new_visit_folders:
                print(f"{visit_fp} is missing")
                continue
            images = os.listdir(visit_fp)
            new_images = os.listdir(new_visit_fp)

            for image in images:
                image_fp = os.path.join(visit_fp, image)
                new_image_fp = os.path.join(new_visit_fp, image)
                if image not in new_images:
                    if image[-6:] != "TN.png":
                        print(f"{image_fp} is missing")

    print("Check completed successfully")

run_check()
