import os
import shutil
import subprocess
import sys
import csv

sys.path.insert(0, '../../scripts')
from common_aDNA_scripts import *

def generate_fastq_patterns(file_paths):
    patterns = {}
    
    for path in file_paths:
        # Extract the filename
        filename = os.path.basename(path)
        
        # Extract the prefix (C1, C2, C3)
        prefix = filename.split('_')[0]
        
        # Store the wildcard pattern
        patterns[prefix] = f"{prefix}*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}"

        prefix = f"{filename.split('_')[0]}_{filename.split('_')[1]}"

        patterns[prefix] = f"{prefix}*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}"

    return patterns

def prepare():
    print_info("Preparing Bger for ref genome mapping")

    # find all raw fastq files
    duplicates_removed_folder = get_folder_path_species_processed_duplicates_removed(FOLDER_BGER)
    fastq_files = get_files_in_folder_matching_pattern(duplicates_removed_folder, f"*{FILE_ENDING_DUPLICATES_REMOVED_FASTQ_GZ}")

    # if no files are found, exit
    if len(fastq_files) == 0:
        print_error("No duplicate removed fastq files found. Exiting.")
        return
    
    for prefix, pattern in generate_fastq_patterns(fastq_files).items():
        fastq_files_per_pattern = get_files_in_folder_matching_pattern(duplicates_removed_folder, pattern)
        print_info(f"Found {len(fastq_files_per_pattern)} fastq files for pattern {pattern}")

        output_folder = get_folder_path_species_processed_prepared_for_ref_genome(FOLDER_BGER)
        output_file_path = os.path.join(output_folder,f"{prefix}_{FILE_ENDING_FASTQ_GZ}")

        if os.path.exists(output_file_path):
            print_info(f"Output file {output_file_path} already exists. Skipping.")
            continue

        # call cat via subprocess
        try:
            print_info(f"Concatenating {len(fastq_files_per_pattern)} fastq files for pattern {pattern}")
            cat_command = f"cat {fastq_files_per_pattern} > {output_file_path}"
            subprocess.run(cat_command, shell=True, check=True)
            print_success(f"Concatenation for pattern {pattern} complete")
        except Exception as e:
            print_error(f"Failed to concatenate fastq files for pattern {pattern}: {e}")


def read_csv(file_path):
    data = {}

    # check if file exists
    if not os.path.exists(file_path):
        raise Exception(f"File {file_path} does not exist")

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data[row[0]] = row[1]
    return data

def get_mapping_runID_to_name():
   
    return read_csv( os.path.join(get_folder_path_species_resources(FOLDER_BGER), MAPPING_FILENAME_RUNID_TO_NAME))

def get_mapping_folder_to_lane():
    return read_csv( os.path.join(get_folder_path_species_resources(FOLDER_BGER), MAPPING_FILENAME_FOLDER_TO_LANE))

# def get_value(data, key):
#     return data.get(key)

# # Example usage:
# file_path = 'example.csv'
# data = read_csv(file_path)
# value = get_value(data, 'key')
# print(value)

def find_fastq_files(directory):
    command = f'find {directory} -type f \\( -name "*_R1_*.fastq.gz" -o -name "*_R2_*.fastq.gz" \\) ! -path "*/undetermined/*"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.splitlines()

def move_file(source_path,target_path,new_filename=None):
    # Check if source file exists
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file '{source_path}' does not exist")

    # Get the filename from the source path
    filename = os.path.basename(source_path)

    # If a new filename is provided, use it
    if new_filename:
        filename = new_filename

    # Construct the target path with the new filename
    target_file_path = os.path.join(target_path, filename)

    # Check if the target file already exists
    if os.path.exists(target_file_path):
        raise FileExistsError(f"Target file '{target_file_path}' already exists")

    # Move the file
    shutil.move(source_path, target_file_path)

    print_info(f"File moved from '{source_path}' to '{target_file_path}'")