# Read in the following file: /Users/user/projects/AutoZebrafish/Detector training/ImageAnnotation/sample_files_list.txt
# For each file in this list, copy the file and move it to a new directory: /Volumes/RFS/Triggerfish Navigation/Zebrafish/annotation/
# Keep the folder structure after allframes/ and before the file name

import os
import shutil

source_file = "/Users/user/projects/AutoZebrafish/Detector training/ImageAnnotation/sample_files_list.txt"
destination_dir = "/Volumes/RFS/Triggerfish Navigation/Zebrafish/annotation/"

with open(source_file, "r") as file:
    for line in file:
        file_path = line.strip()
        if os.path.isfile(file_path):
            folder_path = os.path.dirname(file_path)
            folder_structure = folder_path.split("allframes/")[1]
            destination_folder = os.path.join(destination_dir, folder_structure)
            os.makedirs(destination_folder, exist_ok=True)
            shutil.copy(file_path, destination_folder)
