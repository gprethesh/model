import zipfile
import hashlib
import csv
import os
import zipfile
import hashlib
import csv
import os
import redis
import json
import shutil
import time
import torch
import torch.nn as nn
import torch.optim as optim
import shutil


def validate_uploaded_file(zip_file_path):
    # Add malware validation logic here
    # You may use external tools or implement your own validation
    # Example: Check if the file contains any executable scripts or suspicious files
    # Return True if the file is valid, False otherwise
    return not any(
        file.endswith((".exe", ".bat", ".sh"))
        for file in zipfile.ZipFile(zip_file_path, "r").namelist()
    )


def upload_to_cloud_storage(zip_file_path, cloud_storage_folder):
    # You may replace this with your preferred cloud storage solution
    drive_file_path = os.path.join(
        cloud_storage_folder, os.path.basename(zip_file_path)
    )

    try:
        # Move the file to the cloud storage folder
        shutil.move(zip_file_path, drive_file_path)
        print(f"Moved '{zip_file_path}' to '{drive_file_path}'")
    except FileNotFoundError:
        print(f"Error: File not found - '{zip_file_path}'")

    return drive_file_path


def convert_to_10mb_zip(input_folder, output_folder):
    zip_file_name = f"{os.path.basename(input_folder)}.zip"
    zip_file_path = os.path.join(output_folder, zip_file_name)

    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(input_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, input_folder))

    return zip_file_path


# Function to hash a file using SHA-256
def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


# def process_folders_and_store_hash(main_folder, output_folder, csv_file_path):
#     with open(csv_file_path, "w", newline="") as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow(["File Name", "Hash"])

#         for folder_name in os.listdir(main_folder)[
#             :10
#         ]:  # Limit to a maximum of 10 folders
#             folder_path = os.path.join(main_folder, folder_name)
#             if os.path.isdir(folder_path):
#                 # Convert the folder into a 10MB zip file
#                 zip_file_path = convert_to_10mb_zip(folder_path, output_folder)
#                 print(f"Converted '{folder_name}' to '{zip_file_path}'")

#                 # Validate the uploaded file for malware
#                 if validate_uploaded_file(zip_file_path):
#                     # Upload the zip file to cloud storage
#                     cloud_storage_folder = "Upload_Zips"
#                     cloud_file_path = upload_to_cloud_storage(
#                         zip_file_path, cloud_storage_folder
#                     )

#                     # Hash the cloud file and store in CSV file
#                     file_hash = hash_file(cloud_file_path)
#                     csv_writer.writerow([os.path.basename(cloud_file_path), file_hash])
#                     print(f"Hashed '{cloud_file_path}' with SHA-256: {file_hash}")
#                 else:
#                     print(
#                         f"File '{zip_file_path}' contains malware and will be skipped."
#                     )


# # Specify your Google Drive folder and local destination
# drive_folder = "Archive"
# output_folder = "Upload_Zips"
# csv_file_path = "hashed_files.csv"


# # Process folders, convert to 10MB zip, hash, and store in CSV
# process_folders_and_store_hash(drive_folder, output_folder, csv_file_path)
